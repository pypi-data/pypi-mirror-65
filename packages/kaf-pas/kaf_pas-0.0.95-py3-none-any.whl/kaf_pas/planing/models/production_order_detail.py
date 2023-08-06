import logging

from django.conf import settings
from django.db.models import Sum

from isc_common.number import DelProps
from kaf_pas.planing.models.operations import OperationsManager, OperationsQuerySet
from kaf_pas.planing.models.operations_view import Operations_view

logger = logging.getLogger(__name__)


class Production_order_detailQuerySet(OperationsQuerySet):
    pass


class Production_order_detailManager(OperationsManager):
    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'num': record.id,
            'date': record.date,
            'prev_status_id': record.prev_status.id if record.prev_status else None,
            'production_operation__full_name': record.production_operation.full_name if record.production_operation else None,
            'production_operation__name': record.production_operation.name if record.production_operation else None,
            'production_operation_edizm__name': record.production_operation_edizm.name if record.production_operation_edizm else None,
            'production_operation_edizm_id': record.production_operation_edizm.id if record.production_operation_edizm else None,
            'production_operation_id': record.production_operation.id if record.production_operation else None,
            'production_operation_num': record.production_operation_num,
            'production_operation_qty': record.production_operation_qty,
            'production_operation_attrs': record.production_operation.attrs if record.production_operation else None,
            'launch_id': record.launch.id if record.launch else None,
            'location__code': record.resource.location.code if record.resource and record.resource else None,
            'location__full_name': record.resource.location.full_name if record.resource and record.resource else None,
            'location__name': record.resource.location.name if record.resource and record.resource else None,
            'location_id': record.resource.location.id if record.resource else None,
            'resource__code': record.resource.code if record.resource and record.resource else None,
            'resource__name': record.resource.name if record.resource and record.resource else None,
            'resource__description': record.resource.description if record.resource and record.resource else None,
            'resource_id': record.resource.id if record.resource else None,
            'value': record.value.value if record.value else None,
            'value_start': record.value_start,
            'value_made': record.value_made,
            'description': record.description,
            'edizm__code': record.value.edizm.code if record.value and record.value.edizm else None,
            'edizm__name': record.value.edizm.name if record.value and record.value.edizm else None,
            'edizm_id': record.value.edizm.id if record.value and record.value.edizm else None,
        }
        return DelProps(res)

    def get_queryset(self):
        return Production_order_detailQuerySet(self.model, using=self._db)


class Production_order_detail(Operations_view):
    @property
    def get_status(self):
        return self.status

    @property
    def value_start(self):
        from kaf_pas.planing.models.operation_refs import Operation_refs
        try:
            res = Operation_refs.objects.get(child_id=self.id, parent__opertype__code='PRD_TSK')
            value_start = res.parent.value_start
            return value_start
        except Operation_refs.DoesNotExist:
            return 0

    @property
    def value_made(self):
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.models.operation_value import Operation_value

        operations = [child.child_id for child in Operation_refs.objects.filter(parent_id=self.id, child__opertype=settings.OPERS_TYPES_STACK.MADE_OPERATIONS_TASK)]
        res = Operation_value.objects.filter(operation_id__in=operations).aggregate(Sum('value'))
        sum = res.get('value__sum')
        return sum if sum != None else 0

    @property
    def value_per_one(self):
        from kaf_pas.planing.models.operation_value import Operation_value
        try:
            return Operation_value.objects.get(operation_id=self.id, props=Operation_value.props.perone).value
        except Operation_value.DoesNotExist:
            return 0


    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return self.__str__()

    class Meta:
        proxy = True
        verbose_name = 'Заказы на производство'
