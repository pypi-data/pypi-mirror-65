import logging

from django.db.models import BigIntegerField, BooleanField, PositiveIntegerField

from isc_common.common.mat_views import create_view
from isc_common.datetime import DateToStr
from isc_common.fields.code_field import CodeField
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditQuerySet, AuditManager
from isc_common.models.base_ref import Hierarcy
from isc_common.number import DelProps
from kaf_pas.ckk.models.item import Item_add
from kaf_pas.ckk.models.item_line import Item_lineManager
from kaf_pas.ckk.models.item_refs import Item_refsManager
from kaf_pas.kd.models.document_attributes import Document_attributes
from kaf_pas.kd.models.documents import Documents

logger = logging.getLogger(__name__)


class Tmp_Item_operations_viewQuerySet(AuditQuerySet):
    pass


class Tmp_Item_operations_viewManager(AuditManager):
    @staticmethod
    def create():
        create_view(
            view_name='ckk_tmp_item_operations_view',
            sql_str='''SELECT ckk_item.id,
                               ckk_item.editing,
                               ckk_item.deliting,
                               ckk_item.lastmodified,
                               ckk_item."STMP_1_id",
                               ckk_item."STMP_2_id",
                               ckk_item.props,
                               ckk_item.document_id,
                               ckk_item.deleted_at,
                               ckk_item.parent_id,
                               ckk_item.child_id,
                               ckk_item.relevant,
                               ckk_item.confirmed,
                               CASE
                                   WHEN ckk_item.from_cdw IS NOT NULL THEN ckk_item.from_cdw
                                   WHEN ckk_item.from_spw IS NOT NULL THEN ckk_item.from_spw
                                   WHEN ckk_item.from_pdf IS NOT NULL THEN ckk_item.from_pdf
                                   WHEN ckk_item.man_input IS NOT NULL THEN ckk_item.man_input
                                   WHEN ckk_item.copied IS NOT NULL THEN ckk_item.copied
                                   WHEN ckk_item.on_activated IS NOT NULL THEN ckk_item.on_activated
                                   WHEN ckk_item.from_lotsman IS NOT NULL THEN ckk_item.from_lotsman
                                   ELSE NULL::text
                                   END AS where_from,
                               ckk_item.for_line,
                               ckk_item."isFolder",
                               ckk_item.version,
                               ckk_item.qty_operations,
                               ckk_item.section,
                               ckk_item.refs_props,
                               ckk_item.refs_id
                        FROM (SELECT ckk_item_1.id,
                                     ckk_item_1.editing,
                                     ckk_item_1.deliting,
                                     ckk_item_1.lastmodified,
                                     ckk_item_1."STMP_1_id",
                                     ckk_item_1."STMP_2_id",
                                     ckk_item_1.props,
                                     ckk_item_1.document_id,
                                     ckk_item_1.deleted_at,
                                     ckk_item_1.version,
                                     refs1.id                                   AS refs_id,
                                     refs1.parent_id,
                                     refs1.props                                AS refs_props,
                                     (SELECT DISTINCT ckk_item_line.section
                                      FROM ckk_item_line
                                      WHERE ckk_item_line.parent_id = refs1.parent_id
                                        AND ckk_item_line.child_id = refs1.child_id
                                      LIMIT 1)                                  AS section,
                                     refs1.child_id,
                                     CASE
                                         WHEN ((SELECT count(1) AS count
                                                FROM ckk_item_refs
                                                WHERE ckk_item_refs.parent_id = ckk_item_1.id)) > 0 THEN true
                                         ELSE false
                                         END                                    AS "isFolder",
                                     relevant_column(ckk_item_1.props::integer) AS relevant,
                                     confirmed_column(ckk_item_1.props::integer) AS confirmed,
                                     CASE
                                         WHEN is_bit_on(ckk_item_1.props::integer, 0) THEN 'Первоначально создано'::text
                                         ELSE NULL::text
                                         END                                    AS on_activated,
                                     CASE
                                         WHEN is_bit_on(ckk_item_1.props::integer, 1) THEN 'Получено из чертежа'::text
                                         ELSE NULL::text
                                         END                                    AS from_cdw,
                                     CASE
                                         WHEN is_bit_on(ckk_item_1.props::integer, 2) THEN 'Получено из спецификации'::text
                                         ELSE NULL::text
                                         END                                    AS from_spw,
                                     CASE
                                         WHEN is_bit_on(ckk_item_1.props::integer, 3) THEN 'Строка спецификации'::text
                                         ELSE NULL::text
                                         END                                    AS for_line,
                                     CASE
                                         WHEN is_bit_on(ckk_item_1.props::integer, 4) THEN 'Получено из бумажного архива'::text
                                         ELSE NULL::text
                                         END                                    AS from_pdf,
                                     CASE
                                         WHEN is_bit_on(ckk_item_1.props::integer, 5) THEN 'Занесено вручную'::text
                                         ELSE NULL::text
                                         END                                    AS man_input,
                                     CASE
                                         WHEN is_bit_on(ckk_item_1.props::integer, 6) THEN 'Скопировано'::text
                                         ELSE NULL::text
                                         END                                    AS copied,
                                     CASE
                                         WHEN is_bit_on(ckk_item_1.props::integer, 7) THEN 'Получено из Лоцмана'::text
                                         ELSE NULL::text
                                         END                                    AS from_lotsman,
                                     (SELECT count(*) AS count
                                      FROM production_operations_item poi
                                      WHERE poi.item_id = ckk_item_1.id)        AS qty_operations
                              FROM ckk_item ckk_item_1
                                       JOIN ckk_tmp_item_refs refs1 ON ckk_item_1.id = refs1.child_id) ckk_item'''
        )

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'refs_id': record.refs_id,
            'STMP_1_id': record.STMP_1.id if record.STMP_1 else None,
            'STMP_1__value_str': record.STMP_1.value_str if record.STMP_1 else None,
            'STMP_2_id': record.STMP_2.id if record.STMP_2 else None,
            'STMP_2__value_str': record.STMP_2.value_str if record.STMP_2 else None,
            'lastmodified': DateToStr(record.lastmodified, mask='%Y-%m-%dT%H:%M:%S'),
            'document_id': record.document.id if record.document else None,
            'document__file_document': record.document.file_document if record.document else None,
            'parent_id': record.parent_id,
            'editing': record.editing,
            'deliting': record.deliting,
            'isFolder': record.isFolder,
            'relevant': record.relevant,
            'confirmed': record.confirmed,
            'version': record.version,
            'section': record.section,
            'where_from': record.where_from,
            'qty_operations': record.qty_operations,
            'icon': Item_lineManager.getIcon(record),
            'props': record.props,
            'used': record.refs_props.used,
            'refs_props': record.refs_props,
        }
        # print(res)
        return DelProps(res)

    def get_queryset(self):
        return Tmp_Item_operations_viewQuerySet(self.model, using=self._db)


class Tmp_Item_operations_view(Hierarcy):
    STMP_1 = ForeignKeyProtect(Document_attributes, verbose_name='Наименование изделия', related_name='tmp_STMP_1_view_operations', null=True, blank=True)
    STMP_2 = ForeignKeyProtect(Document_attributes, verbose_name='Обозначение изделия', related_name='tmp_STMP_2_view_operations', null=True, blank=True)
    document = ForeignKeyProtect(Documents, verbose_name='Документ', null=True, blank=True)
    refs_id = BigIntegerField()
    relevant = NameField()
    confirmed = NameField()
    where_from = NameField()
    props = Item_add.get_prop_field()
    refs_props = Item_refsManager.props()
    version = PositiveIntegerField(null=True, blank=True)
    qty_operations = PositiveIntegerField()
    section = CodeField(null=True, blank=True)

    isFolder = BooleanField()

    objects = Tmp_Item_operations_viewManager()

    @property
    def item(self):
        from kaf_pas.ckk.models.item import Item
        return Item.objects.get(id=self.id)

    def __str__(self):
        return f'ID={self.id} STMP_1=[{self.STMP_1}], STMP_2=[{self.STMP_2}], props={self.props}'

    class Meta:
        managed = False
        db_table = 'ckk_tmp_item_operations_view'
        verbose_name = 'Товарная позиция'
