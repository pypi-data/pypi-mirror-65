import logging

from django.db import ProgrammingError

logger = logging.getLogger(__name__)


class Operation_Stack:
    def get_first_item_of_tuple(self, tp):
        res, _ = tp
        return res

    def __init__(self):
        from kaf_pas.production.models.resource import Resource

        try:
            from kaf_pas.production.models.operations import Operations
            self.NOOP = self.get_first_item_of_tuple(Operations.objects.update_or_create(code='00', defaults=dict(
                name='Пустая операция',
                editing=False,
                deliting=False,
            )))

            from kaf_pas.ckk.models.locations import Locations
            self.NO_WORKSHOP = self.get_first_item_of_tuple(Locations.objects.update_or_create(code='00', defaults=dict(
                name='Фиктивный цех',
                editing=False,
                deliting=False,
            )))

            self.NOT_UNDEFINED_WORKSHOP = lambda location: Resource.objects.get_or_create(
                location=location,
                code='none',
                defaults=dict(
                    name='Не определен'
                )
            )


        except ProgrammingError as ex:
            logger.warning(ex)
