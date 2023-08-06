import logging
import sys
from datetime import datetime

from django.conf import settings
from django.db import transaction
from django.db.models import Sum
from django.forms import model_to_dict

from isc_common.http.DSRequest import DSRequest
from isc_common.number import DelProps
from kaf_pas.planing.models.operations import OperationsManager, OperationsQuerySet
from kaf_pas.planing.models.operations_view import Operations_view

logger = logging.getLogger(__name__)


class Production_orderQuerySet(OperationsQuerySet):
    def get_checkStatus(self, request, *args):
        from kaf_pas.planing.models.operations import Operations
        from kaf_pas.planing.models.status_operation_types import Status_operation_types

        request = DSRequest(request=request)
        data = request.json.get('data')
        status__code = data.get('status__code')
        status__name = data.get('status__name')
        id = data.get('id')
        if status__code == 'in_job':
            return dict(status__code=status__code, status__name=status__name, input='closed')
        else:
            operation = Operations.objects.get(id=id)
            operation.prev_status = operation.status
            operation.status = Status_operation_types.objects.get(code='in_job')
            operation.save()
            return dict(status__code=operation.status.code, status__name=operation.status.wrap_name, input='opened')

    def get_setPrevStatus(self, request, *args):
        from kaf_pas.planing.models.operations import Operations

        request = DSRequest(request=request)
        data = request.json.get('data')
        status__code = data.get('status__code')

        if status__code in ["started", "started_partly"]:
            operation = Operations.objects.get(id=id)
            return dict(status__code=operation.status.code, status__name=operation.status.wrap_name, input='opened')

        id = data.get('id')
        if status__code == 'in_job':
            operation = Operations.objects.get(id=id)
            operation.status = operation.prev_status
            operation.save()
            return dict(status__code=operation.status.code, status__name=operation.status.wrap_name, input='opened')

    def _checkEnableQty(self, data):
        qty = data.get('qty')
        if data.get('qty') == None:
            raise Exception('Не введено количество.')
        production_order = Production_order.objects.get(id=data.get('id'))
        value_made = production_order.value_made
        if qty < value_made:
            raise Exception('Превышение существующего количества выпуска.')

    def get_setStartStatus(self, request, *args):
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.models.operation_value import Operation_value
        from kaf_pas.planing.models.operations import Operations

        request = DSRequest(request=request)
        data = request.json.get('data')

        self._checkEnableQty(data)
        with transaction.atomic():
            try:
                res = Operation_refs.objects.get(parent_id=data.get('id'), child__opertype__code='LAUNCH_TSK')
                Operation_value.objects.update_or_create(operation=res.child, defaults=dict(value=data.get('qty')))
                res = model_to_dict(res.parent)
                data.update(res)
                return data
            except Operation_refs.DoesNotExist:
                res = Operations.objects.create(
                    opertype=settings.OPERS_TYPES_STACK.LAUNCH_TASK,
                    date=datetime.now(),
                    status=settings.OPERS_TYPES_STACK.LAUNCH_TASK_STATUSES.get('new'),
                    creator=request.user
                )

                Operation_refs.objects.create(parent_id=data.get('id'), child=res)
                Operation_value.objects.create(operation=res, edizm_id=data.get('edizm_id'), value=data.get('qty'))
                res = model_to_dict(res)
                data.update(res)
                return data

    def getValue_made(self, request, *args):
        request = DSRequest(request=request)
        data = request.json.get('data')
        production_order = Production_order.objects.get(id=data.get('id'))
        res = production_order.value_made
        return dict(value_made=res)


class Production_orderManager(OperationsManager):
    @staticmethod
    def getRecord(record):
        status = record.get_status
        res = {
            'id': record.id,
            'num': record.num,
            'date': record.date,
            'status__code': status.code,
            'status__name': status.wrap_name,
            'prev_status__code': record.prev_status.code if record.prev_status else None,
            'prev_status__name': record.prev_status.wrap_name if record.prev_status else None,
            'status_id': record.status.id if record.status else None,
            'item__STMP_1__value_str': record.item.STMP_1.value_str if record.item and record.item.STMP_1 and record.item.STMP_1 else None,
            'item__STMP_1_id': record.item.STMP_1.id if record.item and record.item.STMP_1 and record.item.STMP_1 else None,
            'item__STMP_2__value_str': record.item.STMP_2.value_str if record.item and record.item.STMP_2 and record.item.STMP_2 else None,
            'item__STMP_2_id': record.item.STMP_2.id if record.item and record.item.STMP_2 and record.item.STMP_2 else None,
            'item_full_name': record.item_full_name,
            'item_id': record.item.id if record.item else None,
            'item_item_name': record.item.item_name if record.item else None,
            'value': record.value.value if record.value else None,
            'value_start': record.value_start,
            'value_made': record.value_made,
            'creator__short_name': record.creator.get_short_name,
            'launch_id': record.launch.id if record.launch else None,
            'launch__date': record.launch.date if record.launch else None,
            'launch__code': record.launch.code if record.launch else None,
            'launch__name': record.launch.name if record.launch else None,
            'edizm__code': record.value.edizm.code if record.value and record.value.edizm else None,
            'edizm__name': record.value.edizm.name if record.value and record.value.edizm else None,
            'edizm_id': record.value.edizm.id if record.value and record.value.edizm else None,
            'creator_id': record.creator.id,
            'description': record.description,
            'isFolder': False,
        }
        return DelProps(res)

    @staticmethod
    def get_resource_workshop(location_id):
        from kaf_pas.ckk.models.locations import Locations

        res = None
        for location in Locations.objects_tree.get_parents(id=location_id, child_id='id', include_self=False):
            if location.props.isWorkshop == True:
                res = dict(id=location.id, title=location.name, prompt=location.full_name)
                break

        if res == None:
            raise Exception(f'Не обнаружен цех, с признаком "Уровень цеха" для : {Locations.objects.get(id=location_id).full_name}')
        return res

    @staticmethod
    def getRecordLocations(record):
        return Production_orderManager.get_resource_workshop(record.get('resource__location_id'))

    @staticmethod
    def getRecordLevels(record):
        return dict(id=record.get('operation_level_id'), title=record.get('operation_level__name'))

    def get_queryset(self):
        return Production_orderQuerySet(self.model, using=self._db)


class Production_order(Operations_view):
    from kaf_pas.planing.models.status_operation_types import Status_operation_types

    objects = Production_orderManager()

    try:
        not_ready_2_start = Status_operation_types.objects.get(code='not_ready_2_start')
        ready_2_start = Status_operation_types.objects.get(code='ready_2_start')
        started_partly = Status_operation_types.objects.get(code='started_partly')
        started = Status_operation_types.objects.get(code='started')
    except Exception as ex:
        logger.error(ex)

    @property
    def get_status(self):
        from kaf_pas.accounting.models.buffers import BuffersManager
        from kaf_pas.production.models.launch_item_refs import Launch_item_refs
        from kaf_pas.planing.models.status_operation_types import Status_operation_types
        from kaf_pas.planing.models.operations import Operations

        status = self.status

        def get_ready_status(enabled_start_qty):
            return Status_operation_types.objects.get_or_create(
                code=f'ready_2_start_{enabled_start_qty}',
                defaults=dict(
                    name=f'Готов к запуску: ({enabled_start_qty})',
                    color='green',
                    prop=Status_operation_types.props.blink
                ))

        enabled_start_qty = sys.maxsize
        value_start = self.value_start

        full_start = True

        for launch_item_refs in Launch_item_refs.objects.filter(launch_id=self.launch.id, parent=self.item.id):
            qty_exists = BuffersManager.getValue(item=launch_item_refs.child)
            if qty_exists == None:
                operation = Operations.objects.get(id=self.id)
                operation.status = self.not_ready_2_start
                operation.save()
                return self.not_ready_2_start
            else:
                if qty_exists >= launch_item_refs.qty_per_one * value_start:
                    enabled_start_qty = launch_item_refs.qty_per_one * value_start
                else:
                    full_start = False
                    en = qty_exists // launch_item_refs.qty_per_one
                    if en < enabled_start_qty:
                        enabled_start_qty = en

        operation = Operations.objects.get(id=self.id)
        if enabled_start_qty == sys.maxsize or full_start == True:
            if value_start == 0:
                operation.status = self.ready_2_start
            elif value_start >= self.value.value:
                operation.status = self.started
            elif value_start < self.value.value:
                operation.status = self.started_partly
            else:
                operation.status = self.ready_2_start
        else:
            operation.status = get_ready_status(enabled_start_qty=enabled_start_qty)
        operation.save()
        return operation.status

    @property
    def value_made(self):
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.models.operation_value import Operation_value

        operations = [child.child_id for child in Operation_refs.objects.filter(parent_id=self.id, child__opertype=settings.OPERS_TYPES_STACK.RELEASE_TASK_PLUS)]
        res = Operation_value.objects.filter(operation_id__in=operations).aggregate(Sum('value'))
        sum = res.get('value__sum')
        return sum if sum != None else 0

    @property
    def value_start(self):
        from kaf_pas.planing.models.operations import Operations
        return Operations.objects.get(id=self.id).value_start

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return self.__str__()

    class Meta:
        proxy = True
        verbose_name = 'Заказы на производство'
