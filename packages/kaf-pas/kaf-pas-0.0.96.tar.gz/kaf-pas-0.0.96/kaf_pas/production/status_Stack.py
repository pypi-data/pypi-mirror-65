import logging

from django.db import ProgrammingError

logger = logging.getLogger(__name__)


class Prod_Status_Stack:
    def get_first_item_of_tuple(self, tp):
        res, _ = tp
        return res

    def __init__(self):
        from kaf_pas.ckk.models.attr_type import AttrManager

        try:
            from kaf_pas.production.models.status_launch import Status_launch

            self.FORMIROVANIE = self.get_first_item_of_tuple(Status_launch.objects.update_or_create(code='formirovanie', defaults=dict(
                name='Формирование',
                editing=False,
                deliting=False,
            )))

            self.ROUTMADE = self.get_first_item_of_tuple(Status_launch.objects.update_or_create(code='route_made', defaults=dict(
                name='Выполнена маршрутизация',
                editing=False,
                deliting=False,
            )))

            self.IN_PRODUCTION = self.get_first_item_of_tuple(Status_launch.objects.update_or_create(code='in_production', defaults=dict(
                name='Сформированы заказы на производство',
                editing=False,
                deliting=False,
            )))

            self.CLOSED = self.get_first_item_of_tuple(Status_launch.objects.update_or_create(code='closed', defaults=dict(
                name='Закрыт',
                editing=False,
                deliting=False,
            )))

            AttrManager.get_or_create_attr(attr_codes='operations.paremetrs.color', attr_names='Операции.Параметры.Цвет')

        except ProgrammingError as ex:
            logger.warning(ex)
