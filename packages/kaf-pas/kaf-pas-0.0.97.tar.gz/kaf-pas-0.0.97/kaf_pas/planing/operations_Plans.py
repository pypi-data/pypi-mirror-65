import logging

from django.db import ProgrammingError
from django.forms import model_to_dict

logger = logging.getLogger(__name__)


class Operations_Plan:
    def get_first_item_of_tuple(self, tp):
        res, _ = tp
        return res

    def __init__(self):
        from kaf_pas.planing.models.operation_types import Operation_types
        from kaf_pas.planing.models.operation_types import Operation_typesManager

        try:
            self.OPERSTYPES = [Operation_typesManager.getRecord(opertype) for opertype in Operation_types.objects.all()]

        except ProgrammingError as ex:
            logger.warning(ex)
