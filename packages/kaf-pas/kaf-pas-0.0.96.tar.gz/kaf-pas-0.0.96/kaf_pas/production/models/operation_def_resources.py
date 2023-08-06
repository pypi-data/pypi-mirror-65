import logging

from bitfield import BitField
from django.db import transaction
from django.db.models import UniqueConstraint, Q
from django.forms import model_to_dict

from isc_common import delAttr, setAttr
from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from isc_common.number import DelProps
from kaf_pas.ckk.models.locations import Locations
from kaf_pas.production.models.operations import Operations
from kaf_pas.production.models.resource import Resource

logger = logging.getLogger(__name__)


class Operation_def_resourcesQuerySet(AuditQuerySet):
    def create(self, **kwargs):
        if kwargs.get('resource'):
            setAttr(kwargs, 'resource_id', kwargs.get('resource').id)
            delAttr(kwargs, 'resource')

        if kwargs.get('location'):
            setAttr(kwargs, 'location_id', kwargs.get('location').id)
            delAttr(kwargs, 'location')

        if not kwargs.get('resource_id') and not kwargs.get('location_id'):
            raise Exception('Необходим хотябы один выбранный параметр.')
        delAttr(kwargs, 'resource__name')
        delAttr(kwargs, 'location__full_name')

        resource_id = kwargs.get('resource_id')
        if resource_id:
            setAttr(kwargs, 'location_id', Resource.objects.get(id=resource_id).location.id)

        return super().create(**kwargs)

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Operation_def_resourcesManager(AuditManager):

    def allUpdateFromRequest(self, request):
        from kaf_pas.production.models.operations_item import Operations_item
        from kaf_pas.production.models.operation_resources import Operation_resources

        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)
        data = request.get_data()
        qty = 0

        with transaction.atomic():
            for operation_def_resource in super().filter(id__in=data.get('ids')).select_for_update():
                for operation_item in Operations_item.objects.filter(operation=operation_def_resource.operation):
                    deleted, _ = Operation_resources.objects.filter(operationitem=operation_item).delete()
                    logger.debug(f'Deleted: {deleted}')
                    operation_resource, _ = Operation_resources.objects.get_or_create(
                        operationitem=operation_item,
                        resource=operation_def_resource.resource,
                        location=operation_def_resource.location,
                    )
                    logger.debug(f'Created: {operation_resource}')
                qty += 1

        return qty

    def updateFromRequest(self, request):
        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()

        resource = None
        location = None

        if _data.get('resource_id') != None:
            resource = Resource.objects.get(id=_data.get('resource_id'))
            location = Locations.objects.get(id=resource.location.id)
            setAttr(_data, 'location_id', location.id)
            setAttr(_data, 'resource_id', resource.id)
        else:
            delAttr(_data, 'resource')

        if resource == None and _data.get('location_id') != None:
            location = Locations.objects.get(id=_data.get('location_id'))
            setAttr(_data, 'location_id', location.id)

        if resource == None and location == None:
            raise Exception('Необходим хотябы один выбранный параметр.')

        delAttr(_data, 'id')
        delAttr(_data, 'resource__code')
        delAttr(_data, 'resource__name')
        delAttr(_data, 'location__code')
        delAttr(_data, 'location__name')
        delAttr(_data, 'location__full_name')
        delAttr(_data, 'complex_name')
        delAttr(_data, 'rec_default')
        res, created = super().update_or_create(id=request.get_id(), defaults=_data)
        setAttr(data, 'id', res.id)
        return data

    def createFromRequest(self, request):
        from kaf_pas.production.models.operations_item import Operations_item
        from kaf_pas.production.models.operation_resources import Operation_resources

        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()
        rec_default = _data.get('rec_default')
        delAttr(_data, 'rec_default')
        operation_id = _data.get('operation_id')

        res = []

        def rec_defaults(operation, operation_resource):
            if rec_default:
                for operationitem in Operations_item.objects.filter(operation_id=operation):
                    if Operation_resources.objects.filter(operationitem=operationitem).count() == 0:
                        operation_resources, created = Operation_resources.objects.get_or_create(
                            operationitem=operationitem,
                            location=operation_resource.location,
                            resource=operation_resource.resource,
                        )
                        if created:
                            logger.debug(f'operation_resources: {operation_resources}')

        if isinstance(operation_id, list):
            delAttr(_data, 'operation_id')
            with transaction.atomic():
                for operation in operation_id:
                    setAttr(_data, 'operation_id', operation)
                    operation_resource = super().create(**_data)
                    _res = DelProps(model_to_dict(operation_resource))
                    setAttr(_res, 'location__full_name', operation_resource.location.full_name if operation_resource.location else None)
                    setAttr(_res, 'resource__name', operation_resource.resource.full_name if operation_resource.resource else None)
                    res.append(_res)

                    rec_defaults(operation=operation, operation_resource=operation_resource)
        else:
            with transaction.atomic():
                operation_resource = super().create(**_data)
                _res = DelProps(model_to_dict(operation_resource))
                setAttr(_res, 'location__full_name', operation_resource.location.full_name if operation_resource.location else None)
                setAttr(_res, 'resource__name', operation_resource.resource.full_name if operation_resource.resource else None)
                res.append(_res)
                rec_defaults(operation=operation_id, operation_resource=operation_resource)
        return res

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'operation_id': record.operation.id,
            'resource_id': record.resource.id if record.resource else None,
            'resource__code': record.resource.code if record.resource else None,
            'resource__name': record.resource.name if record.resource else None,
            'location_id': record.location.id if record.location else None,
            'location__code': record.location.code if record.location else None,
            'location__name': record.location.name if record.location else None,
            'location__full_name': record.location.full_name if record.location else None,
            'complex_name': record.complex_name,
            'editing': record.editing,
            'deliting': record.deliting,
            'rec_default': record.props.rec_default,
            'props': record.props,
        }
        return DelProps(res)

    @staticmethod
    def props():
        return BitField(flags=(
            ('rec_default', 'Записать ресурс по умолчанию на все операции на которых нет ресурсов'),  # 1
        ), default=0, db_index=True)

    def get_queryset(self):
        return Operation_def_resourcesQuerySet(self.model, using=self._db)


class Operation_def_resources(AuditModel):
    operation = ForeignKeyCascade(Operations)
    resource = ForeignKeyProtect(Resource, null=True, blank=True)
    location = ForeignKeyProtect(Locations, null=True, blank=True)
    props = Operation_def_resourcesManager.props()

    @property
    def complex_name(self):
        return f'{self.resource.location.full_name}{self.resource.name}' if self.resource else None

    objects = Operation_def_resourcesManager()

    def __str__(self):
        return f"ID: {self.id}"

    class Meta:
        verbose_name = 'Кросс таблица'
        constraints = [
            UniqueConstraint(fields=['operation'], condition=Q(location=None) & Q(resource=None), name='Operation_def_resources_unique_constraint_0'),
            UniqueConstraint(fields=['operation', 'resource'], condition=Q(location=None), name='Operation_def_resources_unique_constraint_1'),
            UniqueConstraint(fields=['location', 'operation'], condition=Q(resource=None), name='Operation_def_resources_unique_constraint_2'),
            UniqueConstraint(fields=['location', 'operation', 'resource'], name='Operation_def_resources_unique_constraint_3'),
        ]
