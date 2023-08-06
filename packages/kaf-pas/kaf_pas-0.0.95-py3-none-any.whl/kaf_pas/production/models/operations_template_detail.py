import logging

from django.db.models import PositiveIntegerField, TextField

from isc_common.fields.related import ForeignKeyCascade, ForeignKeyProtect
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsManager, CommonManagetWithLookUpFieldsQuerySet
from isc_common.models.audit import AuditModel
from kaf_pas.ckk.models.ed_izm import Ed_izm
from kaf_pas.production.models.operations import Operations
from kaf_pas.production.models.operations_template import Operations_template

logger = logging.getLogger(__name__)


class Operations_template_detailQuerySet(CommonManagetWithLookUpFieldsQuerySet):
    def delete(self):
        return super().delete()

    def create(self, **kwargs):
        return super().create(**kwargs)

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Operations_template_detailManager(CommonManagetWithLookUpFieldsManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'operation_id': record.operation.id,
            'operation__code': record.operation.code,
            'operation__name': record.operation.name,
            'operation__full_name': record.operation.full_name,
            'operation__description': record.operation.description,
            'ed_izm_id': record.ed_izm.id if record.ed_izm else None,
            'ed_izm__code': record.ed_izm.code if record.ed_izm else None,
            'ed_izm__name': record.ed_izm.name if record.ed_izm else None,
            'ed_izm__description': record.ed_izm.description if record.ed_izm else None,
            'qty': record.qty,
            'num': record.num,
            'description': record.description,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Operations_template_detailQuerySet(self.model, using=self._db)


class Operations_template_detail(AuditModel):
    operation = ForeignKeyCascade(Operations)
    num = PositiveIntegerField(default=None, null=True, blank=True)
    qty = PositiveIntegerField(default=None, null=True, blank=True)
    description = TextField(default=None, null=True, blank=True)
    ed_izm = ForeignKeyProtect(Ed_izm, default=None, null=True, blank=True)
    template = ForeignKeyCascade(Operations_template)

    objects = Operations_template_detailManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Детализация шаблона группы оперций'
        unique_together = (('operation', 'template'),)
