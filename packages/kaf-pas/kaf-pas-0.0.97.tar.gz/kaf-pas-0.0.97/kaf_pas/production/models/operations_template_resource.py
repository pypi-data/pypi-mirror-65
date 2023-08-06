import logging

from django.conf import settings
from django.db import transaction, connection
from django.db.models import PositiveIntegerField, OneToOneField, CASCADE, UniqueConstraint, Q
from django.forms import model_to_dict

from isc_common import delAttr, setAttr
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsManager, CommonManagetWithLookUpFieldsQuerySet
from isc_common.models.audit import AuditModel
from kaf_pas.ckk.models.locations import Locations
from kaf_pas.production.models.operations_template_detail import Operations_template_detail
from kaf_pas.production.models.resource import Resource

logger = logging.getLogger(__name__)


class Operations_template_resourceQuerySet(CommonManagetWithLookUpFieldsQuerySet):
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

        setAttr(kwargs, '_operation', 'create')
        return super().create(**kwargs)

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Operations_template_resourceManager(CommonManagetWithLookUpFieldsManager):

    @staticmethod
    def refresh_resource(apps=None, schema_editor=None):
        settings.LOCKS.acquire('Operations_template_resourceManager.refresh_resource')
        sql_text = '''select  template_id, count(*)
                    from production_operations_template_resource
                    group by template_id
                    having count(*) > 1'''

        sql_items = f'''select id
            from production_operations_template_resource
            where template_id = %s'''

        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(sql_text)
                rows = cursor.fetchall()
                for row in rows:
                    template_id, count = row
                    # print(f'launch_template_id: {launch_template_id}')
                    cursor.execute(sql_items, [template_id])
                    rows_item = cursor.fetchall()

                    first_step = True
                    for item in rows_item:
                        id, = item
                        if not first_step:
                            # print(f'id: {id}')
                            res = Operations_template_resource.objects.filter(id=id).delete()
                            # print(res)
                        else:
                            first_step = False
        settings.LOCKS.release('Operations_template_resourceManager.refresh_resource')

    def createFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()
        template_id = _data.get('template_id')

        res = []
        if isinstance(template_id, list):
            delAttr(_data, 'template_id')
            with transaction.atomic():
                for template in template_id:
                    setAttr(_data, 'template_id', template)
                    delAttr(_data, 'location__full_name')
                    delAttr(_data, 'resource__name')
                    operation_resource, created = super().get_or_create(**_data)
                    if created:
                        _res = model_to_dict(operation_resource)
                        setAttr(_res, 'location__full_name', operation_resource.location.full_name if operation_resource.location else None)
                        setAttr(_res, 'resource__name', operation_resource.resource.full_name if operation_resource.resource else None)
                        res.append(_res)
        else:
            delAttr(_data, 'location__full_name')
            delAttr(_data, 'resource__name')
            operation_resource, created = super().get_or_create(**_data)
            if created:
                _res = model_to_dict(operation_resource)
                setAttr(_res, 'location__full_name', operation_resource.location.full_name if operation_resource.location else None)
                setAttr(_res, 'resource__name', operation_resource.resource.full_name if operation_resource.resource else None)
                res.append(_res)
        return res

    def updateFromRequest(self, request, removed=None, function=None):
        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)
        data = request.get_data()

        self._remove_prop(data, removed)
        _data = self.clone_data(data)
        delAttr(_data, 'id')
        res = super().filter(id=data.get('id')).update(**_data)
        return res

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'template_id': record.template.id if record.template else None,
            'resource_id': record.resource.id if record.resource else None,
            'resource__code': record.resource.code if record.resource else None,
            'resource__name': record.resource.name if record.resource else None,
            'location_id': record.location.id if record.location else None,
            'location__code': record.location.code if record.location else None,
            'location__name': record.location.name if record.location else None,
            'location__full_name': record.location.full_name if record.location else None,
            'complex_name': record.complex_name,
            'batch_size': record.batch_size,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Operations_template_resourceQuerySet(self.model, using=self._db)


class Operations_template_resource(AuditModel):
    template = OneToOneField(Operations_template_detail, on_delete=CASCADE)
    resource = ForeignKeyProtect(Resource, null=True, blank=True)
    location = ForeignKeyProtect(Locations, null=True, blank=True)
    batch_size = PositiveIntegerField(default=1)

    @property
    def complex_name(self):
        return f'{self.resource.location.full_name}{self.resource.name}' if self.resource else None

    objects = Operations_template_resourceManager()

    def __str__(self):
        return f"{self.id}, template: [{self.template}], resource: [{self.resource}], location: [{self.location}]"

    def __repr__(self):
        return str(self.resource) if self.resource else str(self.location)

    class Meta:
        verbose_name = 'Кросс таблица'
        constraints = [
            UniqueConstraint(fields=['template'], condition=Q(location=None) & Q(resource=None), name='Operations_template_resource_unique_constraint_0'),
            UniqueConstraint(fields=['template', 'resource'], condition=Q(location=None), name='Operations_template_resource_unique_constraint_1'),
            UniqueConstraint(fields=['location', 'template'], condition=Q(resource=None), name='Operations_template_resource_unique_constraint_2'),
            UniqueConstraint(fields=['location', 'template', 'resource'], name='Operations_template_resource_unique_constraint_3'),
        ]
