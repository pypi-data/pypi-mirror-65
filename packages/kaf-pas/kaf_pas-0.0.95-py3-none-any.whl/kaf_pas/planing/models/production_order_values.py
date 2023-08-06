import logging
import sys
from datetime import datetime

from django.conf import settings
from django.db import transaction
from django.db.models import DateTimeField, Sum
from django.forms import model_to_dict

from isc_common.auth.models.user import User
from isc_common.fields.related import ForeignKeyProtect, ForeignKeySetNull
from isc_common.http.DSRequest import DSRequest
from isc_common.models.base_ref import Hierarcy
from isc_common.models.standard_colors import Standard_colors
from isc_common.number import DelProps
from kaf_pas.planing.models.operation_types import Operation_types
from kaf_pas.planing.models.operation_value import Operation_value
from kaf_pas.planing.models.operations import OperationsManager, OperationsQuerySet

logger = logging.getLogger(__name__)


class Production_order_valuesQuerySet(OperationsQuerySet):
    pass


class Production_order_valuesManager(OperationsManager):
    def createFromRequest(self, request, removed=None):
        from kaf_pas.planing.models.operations import Operations
        from kaf_pas.planing.models.production_order_detail import Production_order_detail
        from kaf_pas.ckk.models.ed_izm import Ed_izm

        request = DSRequest(request=request)
        data = request.get_data()
        opertype = request.get_operationtype()

        if not isinstance(data.get('child_ids'), list):
            raise Exception(f'Не выбраны производственные операции(ия).')

        if not isinstance(data.get('parent_id'), int):
            raise Exception(f'Не выбран заказ на производство.')

        if not isinstance(data.get('edizm_id'), int):
            raise Exception(f'Не указана еденница измерения.')

        childs = Production_order_detail.objects.filter(
            id__in=data.get('child_ids'),
            parent_id=data.get('parent_id'),
            opertype=settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_TASK,
            value__props=~Operation_value.props.perone
        )
        value = data.get('value')

        edizm = Ed_izm.objects.get(id=data.get('edizm_id'))

        with transaction.atomic():
            for parent in Operations.objects.select_for_update().filter(id=data.get('parent_id')):
                res = Production_order_valuesManager.makeAll(
                    parent=parent,
                    childs=childs,
                    value=value,
                    opertype=opertype,
                    edizm=edizm,
                    user=request.user
                )

            return res

    # IUD - Insert/Update/Delete
    @staticmethod
    def makeAll(parent, childs, value, opertype, edizm, user):
        from kaf_pas.production.models.launch_item_refs import Launch_item_refs
        from kaf_pas.accounting.models.buffers import BuffersManager
        from kaf_pas.planing.models.operations import Operations
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.models.operation_item import Operation_item
        from kaf_pas.planing.models.operation_launches import Operation_launches
        from kaf_pas.planing.models.production_order_detail import Production_order_detail

        # parent - заказ на производство,
        # childs - производственные операции,
        # value количетвенная операция данной производственной операции
        # opertype - тип REST операции "add", "update" etc

        res = []
        settings.LOCKS.acquire('Production_order_valuesManager.makeAll')
        if opertype == 'add':

            # Определяем позволяет ли остатки в операциях записать их как сделанные
            for child in childs:
                tail = round(child.value_start - child.value_made, 4)
                if value > tail:
                    raise Exception(f'По операции {child.production_operation.full_name} превышен остаток {tail}, а затребовано {round(value, 4)}.')
                else:
                    operations = Operations.objects.create(
                        opertype=settings.OPERS_TYPES_STACK.MADE_OPERATIONS_TASK,
                        date=datetime.now(),
                        status=settings.OPERS_TYPES_STACK.MADE_OPERATIONS_STATUSES.get('new'),
                        creator=user
                    )
                    logger.debug(f'Created operations: {operations}')

                    operation_refs = Operation_refs.objects.create(parent_id=child.id, child=operations)
                    logger.debug(f'Created operation_refs: {operation_refs}')

                    operation_value = Operation_value.objects.create(
                        operation=operations,
                        edizm=edizm,
                        value=value,
                    )
                    logger.debug(f'Created operation_value: {operation_value}')
                    res.append(dict(
                        id=operations.id,
                        date=operations.date,
                        value=operation_value.value,
                        edizm_id=edizm.id,
                        edizm__name=edizm.name,
                        creator__short_name=operations.creator.get_short_name
                    ))

            # Просматриваем все операции на предмет выявления максимального выпуска
            # min_value минимальное возможное оформление выпуска

            def values_not_used_in_release(id):
                return Production_order_values.objects.filter(
                    parent_id=id,
                    value__props=~Operation_value.props.used_in_release,
                    opertype=settings.OPERS_TYPES_STACK.MADE_OPERATIONS_TASK
                )

            min_qty_release = sys.maxsize
            production_order_detail_arr = []
            for production_order_detail in Production_order_detail.objects.filter(
                    parent_id=parent.id,
                    opertype=settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_TASK):

                values_not_used_in_release_sum = values_not_used_in_release(id=production_order_detail.id).aggregate(Sum('value__value')).get('value__value__sum', 0)
                if values_not_used_in_release_sum > 0:
                    min_qty_release_prev = values_not_used_in_release_sum // production_order_detail.value_per_one
                    if min_qty_release_prev == 0:
                        return res
                    else:
                        if min_qty_release > min_qty_release_prev:
                            min_qty_release = min_qty_release_prev
                        production_order_detail_arr.append(production_order_detail)

            # Проверка на наличее в буферах комплектующих
            items = []
            for item in Launch_item_refs.objects.filter(
                    launch=Operation_launches.objects.get(operation=parent).launch,
                    parent=Operation_item.objects.get(operation=parent).item
            ):
                qty_exists = BuffersManager.getValue(item=item.child)
                summa_tot = min_qty_release * item.qty_per_one
                if qty_exists == None:
                    return res
                elif qty_exists < summa_tot:
                    min_qty_release_prev = qty_exists // item.qty_per_one
                    if min_qty_release_prev > 0:
                        min_qty_release = min_qty_release_prev
                        items.append((item, min_qty_release * item.qty_per_one))
                    else:
                        return res
                elif qty_exists > summa_tot:
                    items.append((item, summa_tot))

            for item, value in items:
                # Операция с плюсом по тов позиции выпуска
                res = Operations.objects.create(
                    opertype=settings.OPERS_TYPES_STACK.RELEASE_TASK_MINUS,
                    date=datetime.now(),
                    status=settings.OPERS_TYPES_STACK.RELEASE_TASK_MINUS.get('new'),
                    creator=user
                )

                Operation_item.objects.create(
                    operation=res,
                    item=parent.item,
                    item_full_name=item.full_name,
                    item_full_name_obj=item.full_name_obj
                )

                Operation_refs.objects.create(parent=parent, child=res)
                Operation_value.objects.create(operation=res, edizm=edizm, value=value)

            releases_det_operations = []
            for production_order_detail in production_order_detail_arr:
                total_value = production_order_detail.value * min_qty_release
                for not_used_in_release_used in values_not_used_in_release(id).order_by('value'):
                    if not_used_in_release_used.value <= total_value:
                        operation_value, _ = Operation_value.objects.update_or_create(
                            id=not_used_in_release_used.value.id,
                            defaults=dict(props=Operation_value.props.used_in_release))

                        releases_det_operations.append(operation_value.operation)
                        total_value -= not_used_in_release_used.value
                    else:
                        operation_value = Operation_value.objects.get(id=not_used_in_release_used.value.id)
                        operation_value.props = Operation_value.props.used_in_release
                        operation_value.value = total_value
                        operation_value.save()
                        releases_det_operations.append(operation_value.operation)

                        operation = Operations.objects.get(id=operation_value.operation)
                        res = Operations.objects.create(
                            opertype=operation.opertype,
                            date=operation.date,
                            status=operation.status,
                            creator=operation.user
                        )

                        Operation_refs.objects.create(parent=operation.child, child=res)
                        Operation_value.objects.create(
                            operation=res,
                            edizm=edizm,
                            value=not_used_in_release_used.valu - total_value,
                        )

            first_step = True
            parent_release = None
            for releases_det_operation in releases_det_operations:
                if first_step:
                    parent_release = Operations.objects.create(
                        opertype=settings.OPERS_TYPES_STACK.RELEASE_TASK_PLUS,
                        date=datetime.now(),
                        status=settings.OPERS_TYPES_STACK.RELEASE_TASK_PLUS.get('new'),
                        creator=user
                    )
                    Operation_refs.objects.create(parent=parent, child=parent_release)
                    Operation_value.objects.create(operation=parent_release, edizm=edizm, value=min_qty_release, props=Operation_value.props.used_in_release)

                    Operation_item.objects.create(
                        operation=parent_release,
                        item=parent.item,
                        item_full_name=parent.item.full_name,
                        item_full_name_obj=parent.item.full_name_obj
                    )
                    first_step = False

                Operation_refs.objects.create(parent=parent_release, child=releases_det_operation)
        settings.LOCKS.release('Production_order_valuesManager.makeAll')

        return res

    def deleteFromRequest(self, request, removed=None):
        from kaf_pas.planing.models.operations import Operations
        from kaf_pas.planing.models.operation_refs import Operation_refs

        request = DSRequest(request=request)
        res = 0

        data = request.get_data()
        _transaction = data.get('transaction')
        ids = []
        if _transaction != None:
            operations = _transaction.get('operations')
            ids = [item.get('data').get('id') for item in operations]
        else:
            ids.append(data.get('id'))

        with transaction.atomic():
            for opeartion in Operations.objects.select_for_update().filter(id__in=ids):
                Operation_value.objects.filter(operation=opeartion).delete()
                Operation_refs.objects.filter(child=opeartion).delete()
                opeartion.delete()
        return res

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'color__color': record.color.color if record.color else None,
            'color__name': record.color.name if record.color else None,
            'color_id': record.color.id if record.color else None,
            'creator__short_name': record.creator.get_short_name,
            'creator_id': record.creator.id,
            'date': record.date,
            'edizm__code': record.value.edizm.code if record.value and record.value.edizm else None,
            'edizm__name': record.value.edizm.name if record.value and record.value.edizm else None,
            'edizm_id': record.value.edizm.id if record.value and record.value.edizm else None,
            'value': record.value.value,
            'used_in_release': record.value.props.used_in_release,
        }
        return DelProps(res)

    def get_queryset(self):
        return Production_order_valuesQuerySet(self.model, using=self._db)


class Production_order_values(Hierarcy):
    color = ForeignKeyProtect(Standard_colors, null=True, blank=True)
    opertype = ForeignKeyProtect(Operation_types)
    creator = ForeignKeyProtect(User, default=None)
    date = DateTimeField(default=None)
    value = ForeignKeySetNull(Operation_value, null=True, blank=True, related_name='planing_Production_order_values_view')

    objects = Production_order_valuesManager()

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return self.__str__()

    class Meta:
        managed = False
        db_table = 'planing_operations_values_view'
        verbose_name = 'Списания'
