import logging

from django.db.models import Model

from isc_common.common.mat_views import create_tmp_table
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditQuerySet, AuditManager
from isc_common.models.tree_audit import TreeAuditModelManager
from isc_common.number import DelProps
from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.item_refs import Item_refsManager

logger = logging.getLogger(__name__)


class Tmp_Item_refsQuerySet(AuditQuerySet):
    pass


class Tmp_Item_refsManager(AuditManager):

    @staticmethod
    def create():
        create_tmp_table(
            fields_str='''id bigserial NOT NULL,
                        child_id int8 NOT NULL,
                        parent_id int8 NULL,
                        props int8 NOT NULL,
                        CONSTRAINT "Tmp_Item_refs_not_circulate_refs" CHECK ((NOT (child_id = parent_id))),
                        CONSTRAINT "Tmp_Item_refs_unique" UNIQUE (child_id, parent_id),
                        CONSTRAINT ckk_tmp_item_refs_pkey PRIMARY KEY (id)''',
            unique_indexes=[('child_id', 'parent_id IS NULL')],
            table_name='ckk_tmp_item_refs',
            # on_commit=None,
            drop=False
        )

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'child_id': record.child.id,
            'parent_id': record.parent.id if record.parent else None,
            'used': record.props.used,
        }
        return DelProps(res)

    def get_queryset(self):
        return Tmp_Item_refsQuerySet(self.model, using=self._db)


class Tmp_Item_refs(Model):
    child = ForeignKeyProtect(Item, related_name='tmp_child')
    parent = ForeignKeyProtect(Item, related_name='tmp_parent', blank=True, null=True)

    props = Item_refsManager.props()

    objects = TreeAuditModelManager()

    def __str__(self):
        return f'\nID={self.id}, child=[{self.child}], parent=[{self.parent}]'

    class Meta:
        managed = False
        db_table = 'ckk_tmp_item_refs'
        verbose_name = 'Tmp_Item_refs'
