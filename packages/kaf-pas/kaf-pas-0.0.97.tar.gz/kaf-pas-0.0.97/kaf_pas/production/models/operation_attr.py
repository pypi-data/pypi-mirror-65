import logging

from django.db import transaction

from isc_common import setAttr, delAttr
from isc_common.fields.related import ForeignKeyCascade
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsManager, CommonManagetWithLookUpFieldsQuerySet
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from kaf_pas.ckk.models.attr_type import Attr_type
from kaf_pas.production.models.operations import Operations

logger = logging.getLogger(__name__)


class Operation_attrQuerySet(CommonManagetWithLookUpFieldsQuerySet):
    def create(self, **kwargs):
        operation_id = kwargs.get('operation_id')

        res = None
        with transaction.atomic():
            if isinstance(operation_id, list):
                for op in operation_id:
                    setAttr(kwargs, 'operation_id', op)
                    delAttr(kwargs, 'attr_type__full_name')
                    delAttr(kwargs, 'attr_type__code')
                    delAttr(kwargs, 'attr_type__description')

                    res = super().create(**kwargs)
        return res


class Operation_attrManager(CommonManagetWithLookUpFieldsManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            "attr_type_id": record.attr_type.id,
            "attr_type__code": record.attr_type.code,
            "attr_type__name": record.attr_type.name,
            "attr_type__full_name": record.attr_type.full_name,
            "attr_type__description": record.attr_type.description,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Operation_attrQuerySet(self.model, using=self._db)


class Operation_attr(AuditModel):
    operation = ForeignKeyCascade(Operations)
    attr_type = ForeignKeyCascade(Attr_type)

    objects = Operation_attrManager()

    def __str__(self):
        return f"ID:{self.id}, attr: [{self.attr_type}] , operation: [{self.operation}]"

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Кросс-таблица'
        unique_together = (('operation', 'attr_type'),)
