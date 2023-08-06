import logging

from django.db.models import PositiveIntegerField, BooleanField
from isc_common.common import blinkString
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade, ForeignKeySetNull
from isc_common.models.audit import AuditModel, AuditManager
from isc_common.number import DelProps

from kaf_pas.ckk.models.item import Item_add, Item
from kaf_pas.ckk.models.item_line import Item_line
from kaf_pas.kd.models.document_attributes import Document_attributes
from kaf_pas.production.models.launches import Launches

logger = logging.getLogger(__name__)


class Launch_item_line_viewManager(AuditManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'child_id': record.child.id,
            'parent_id': record.parent.id,
            'SPC_CLM_FORMAT_id': record.SPC_CLM_FORMAT.id if record.SPC_CLM_FORMAT else None,
            'SPC_CLM_FORMAT__value_str': record.SPC_CLM_FORMAT.value_str if record.SPC_CLM_FORMAT else None,
            'SPC_CLM_ZONE_id': record.SPC_CLM_ZONE.id if record.SPC_CLM_ZONE else None,
            'SPC_CLM_ZONE__value_str': record.SPC_CLM_ZONE.value_str if record.SPC_CLM_ZONE else None,
            'SPC_CLM_POS_id': record.SPC_CLM_POS.id if record.SPC_CLM_POS else None,
            'SPC_CLM_POS__value_str': record.SPC_CLM_POS.value_str if record.SPC_CLM_POS else None,
            'SPC_CLM_POS__value_int': record.SPC_CLM_POS.value_int if record.SPC_CLM_POS else None,
            'SPC_CLM_MARK_id': record.SPC_CLM_MARK.id if record.SPC_CLM_MARK else None,
            'SPC_CLM_MARK__value_str': record.SPC_CLM_MARK.value_str if record.SPC_CLM_MARK else None,
            'SPC_CLM_NAME_id': record.SPC_CLM_NAME.id if record.SPC_CLM_NAME else None,
            'SPC_CLM_NAME__value_str': record.SPC_CLM_NAME.value_str if record.SPC_CLM_NAME else None,
            'SPC_CLM_COUNT_id': record.SPC_CLM_COUNT.id if record.SPC_CLM_COUNT else None,
            'SPC_CLM_COUNT__value_str': record.SPC_CLM_COUNT.value_str if record.SPC_CLM_COUNT else None,
            'SPC_CLM_NOTE_id': record.SPC_CLM_NOTE.id if record.SPC_CLM_NOTE else None,
            'SPC_CLM_NOTE__value_str': record.SPC_CLM_NOTE.value_str if record.SPC_CLM_NOTE else None,
            'SPC_CLM_MASSA_id': record.SPC_CLM_MASSA.id if record.SPC_CLM_MASSA else None,
            'SPC_CLM_MASSA__value_str': record.SPC_CLM_MASSA.value_str if record.SPC_CLM_MASSA else None,
            'SPC_CLM_MATERIAL_id': record.SPC_CLM_MATERIAL.id if record.SPC_CLM_MATERIAL else None,
            'SPC_CLM_MATERIAL__value_str': record.SPC_CLM_MATERIAL.value_str if record.SPC_CLM_MATERIAL else None,
            'SPC_CLM_USER_id': record.SPC_CLM_USER.id if record.SPC_CLM_USER else None,
            'SPC_CLM_USER__value_str': record.SPC_CLM_USER.value_str if record.SPC_CLM_USER else None,
            'SPC_CLM_KOD_id': record.SPC_CLM_KOD.id if record.SPC_CLM_KOD else None,
            'SPC_CLM_KOD__value_str': record.SPC_CLM_KOD.value_str if record.SPC_CLM_KOD else None,
            'SPC_CLM_FACTORY_id': record.SPC_CLM_FACTORY.id if record.SPC_CLM_FACTORY else None,
            'SPC_CLM_FACTORY__value_str': record.SPC_CLM_FACTORY.value_str if record.SPC_CLM_FACTORY else None,
            'section': record.section,
            'section_num': record.section_num,
            'subsection': record.subsection,
            'where_from': record.where_from,
            'lastmodified': record.lastmodified,
            'editing': record.editing,
            'deliting': record.deliting,
            'enabled': record.enabled,
            'item_props': record.item_props,
            'relevant': record.relevant,
        }
        return DelProps(res)

    @staticmethod
    def getRecord1(record):
        from kaf_pas.accounting.models.buffers import BuffersManager
        qty = record.SPC_CLM_COUNT.value_int if record.SPC_CLM_COUNT else None
        qty_exists = BuffersManager.getValue(item=record.child)

        status = None
        if record.section != 'Документация':
            if qty_exists == None:
                status = blinkString(text='Полное отсутствие', color='red', bold=True, blink=False)
            elif qty == None:
                status = blinkString(text='Неопределен', bold=True, blink=False)
            elif qty > qty_exists:
                status = blinkString(text='Недостаточно', color='blue', bold=True, blink=False)
            else:
                status = blinkString(text='Достаточно', color='green', bold=True, blink=False)

        res = {
            'id': record.id,
            'child_id': record.child.id,
            'parent_id': record.parent.id,
            'SPC_CLM_MARK_id': record.SPC_CLM_MARK.id if record.SPC_CLM_MARK else None,
            'SPC_CLM_MARK__value_str': record.SPC_CLM_MARK.value_str if record.SPC_CLM_MARK else None,
            'SPC_CLM_NAME_id': record.SPC_CLM_NAME.id if record.SPC_CLM_NAME else None,
            'SPC_CLM_NAME__value_str': record.SPC_CLM_NAME.value_str if record.SPC_CLM_NAME else None,
            'SPC_CLM_COUNT_id': record.SPC_CLM_COUNT.id if record.SPC_CLM_COUNT else None,
            'SPC_CLM_COUNT__value_str': record.SPC_CLM_COUNT.value_str if record.SPC_CLM_COUNT else None,
            'SPC_CLM_COUNT__value_int': qty,
            'qty_per_one': record.qty_per_one,
            'qty_exists': BuffersManager.getValue(item=record.child),
            'section': record.section,
            'section_num': record.section_num,
            'status': status,
            'subsection': record.subsection,
            'where_from': record.where_from,
            'lastmodified': record.lastmodified,
            'editing': record.editing,
            'deliting': record.deliting,
            'enabled': record.enabled,
            'item_props': record.item_props,
            'relevant': record.relevant,
        }
        return DelProps(res)


class Launch_item_line_view(AuditModel):
    parent = ForeignKeyProtect(Item, verbose_name='Товарная позиция', related_name='item_parent_l')
    child = ForeignKeyCascade(Item, verbose_name='Товарная позиция', related_name='item_child_l')

    SPC_CLM_FORMAT = ForeignKeyProtect(Document_attributes, verbose_name='Формат', related_name='SPC_CLM_FORMAT_l', null=True, blank=True)
    SPC_CLM_ZONE = ForeignKeyProtect(Document_attributes, verbose_name='Зона', related_name='SPC_CLM_ZONE_l', null=True, blank=True)
    SPC_CLM_POS = ForeignKeyProtect(Document_attributes, verbose_name='Позиция', related_name='SPC_CLM_POS_l', null=True, blank=True)
    SPC_CLM_MARK = ForeignKeyProtect(Document_attributes, verbose_name='Обозначение', related_name='SPC_CLM_MARK_l', null=True, blank=True)
    SPC_CLM_NAME = ForeignKeyProtect(Document_attributes, verbose_name='Наименование', related_name='SPC_CLM_NAME_l', null=True, blank=True)
    SPC_CLM_COUNT = ForeignKeyProtect(Document_attributes, verbose_name='Количество', related_name='SPC_CLM_COUNT_l', null=True, blank=True)
    SPC_CLM_NOTE = ForeignKeyProtect(Document_attributes, verbose_name='Примечание', related_name='SPC_CLM_NOTE_l', null=True, blank=True)
    SPC_CLM_MASSA = ForeignKeyProtect(Document_attributes, verbose_name='Масса', related_name='SPC_CLM_MASSA_l', null=True, blank=True)
    SPC_CLM_MATERIAL = ForeignKeyProtect(Document_attributes, verbose_name='Материал', related_name='SPC_CLM_MATERIAL_l', null=True, blank=True)
    SPC_CLM_USER = ForeignKeyProtect(Document_attributes, verbose_name='Пользовательская', related_name='SPC_CLM_USER_l', null=True, blank=True)
    SPC_CLM_KOD = ForeignKeyProtect(Document_attributes, verbose_name='Код', related_name='SPC_CLM_KOD_l', null=True, blank=True)
    SPC_CLM_FACTORY = ForeignKeyProtect(Document_attributes, verbose_name='Предприятие - изготовитель', related_name='SPC_CLM_FACTORY_l', null=True, blank=True)
    section = NameField()
    section_num = PositiveIntegerField(default=0)
    subsection = NameField()
    item_line = ForeignKeySetNull(Item_line, null=True, blank=True)
    launch = ForeignKeyProtect(Launches)

    where_from = NameField()
    item_props = Item_add.get_prop_field()
    relevant = NameField()
    enabled = BooleanField()

    @property
    def qty_per_one(self):
        try:
            from kaf_pas.production.models.launch_item_refs import Launch_item_refs
            launch_item_refs = Launch_item_refs.objects.get(launch_id=self.launch.id, child=self.child, parent=self.parent)
            return launch_item_refs.qty_per_one if self.section != 'Документация' else None
        except Launch_item_refs.DoesNotExist:
            return None
        except Launch_item_refs.MultipleObjectsReturned:
            return None

    objects = Launch_item_line_viewManager()

    class Meta:
        verbose_name = 'Строка состава изделия в производственной спецификации'
        db_table = 'production_launch_item_line_view'
        managed = False
        # proxy = True
