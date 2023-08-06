import logging

from bitfield import BitField

from isc_common.fields.name_field import NameStrictField
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsManager, CommonManagetWithLookUpFieldsQuerySet
from isc_common.models.base_ref import BaseRefHierarcy, BaseRefQuerySet
from isc_common.number import DelProps

logger = logging.getLogger(__name__)


class OperationsQuerySet(CommonManagetWithLookUpFieldsQuerySet, BaseRefQuerySet):
    pass


class OperationsManager(CommonManagetWithLookUpFieldsManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'full_name': record.full_name,
            'description': record.description,
            'parent_id': record.parent_id,
            'lastmodified': record.lastmodified,
            'editing': record.editing,
            'deliting': record.deliting,
            'props': record.props,
            'assemly': record.props.assemly,
            'made_common_form': record.props.made_common_form,
        }
        return DelProps(res)

    def get_queryset(self):
        return OperationsQuerySet(self.model, using=self._db)

    @staticmethod
    def get_props():
        return BitField(flags=(
            ('assemly', 'Операция комплектации'),  # 1
            ('made_common_form', 'Формировать общий документ'),  # 1
        ), default=0, db_index=True)


class Operations(BaseRefHierarcy):
    name = NameStrictField()
    props = OperationsManager.get_props()

    @property
    def attrs(self):
        from kaf_pas.production.models.operation_attr import Operation_attr
        return [item.attr_type.code for item in Operation_attr.objects.filter(operation=self)]

    objects = OperationsManager()

    def __str__(self):
        return f'ID={self.id}, code={self.code}, name={self.name}, description={self.description}'

    class Meta:
        verbose_name = 'Операции'
