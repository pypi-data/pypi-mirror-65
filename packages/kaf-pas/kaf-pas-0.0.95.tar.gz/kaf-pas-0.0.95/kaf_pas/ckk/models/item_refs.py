import logging

from bitfield import BitField
from django.db import connection, transaction
from django.db.models import Q, UniqueConstraint, CheckConstraint, F

from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditQuerySet, AuditManager
from isc_common.models.base_ref import Hierarcy
from isc_common.models.tree_audit import TreeAuditModelManager
from isc_common.number import DelProps
from kaf_pas.ckk.models.item import Item

logger = logging.getLogger(__name__)


class Item_refsQuerySet(AuditQuerySet):
    def has_child_entered(self, id):
        with connection.cursor() as cursor:
            cursor.execute('''select count(*)
                                   from ckk_item_refs
                                   where child_id = %s''', [id])
            cnt, = cursor.fetchone()
            return cnt > 0

    def delete(self):
        return super().delete()

    def delete_with_checked(self):
        from kaf_pas.ckk.views.item_view import audo_top_level
        with transaction.atomic():
            for item_ref in self:
                if not self.has_child_entered(id=item_ref.child.id):
                    Item_refs.objects1.create(child=item_ref.child, parent_id=int(audo_top_level))
            return super().delete()

    def get_or_create(self, defaults=None, **kwargs):
        return super().get_or_create(defaults=defaults, **kwargs)


class Item_refsManager(AuditManager):
    @staticmethod
    def props():
        return BitField(flags=(
            ('relevant', 'Актуальность'),  # 1
            ('used', 'Используемость в технологической спецификации'),  # 2
        ), default=3, db_index=True)

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'child_id': record.child.id,
            'parent_id': record.parent.id if record.parent else None,
            'editing': record.editing,
            'deliting': record.deliting,
            'used': record.props.used,
        }
        return DelProps(res)

    def get_queryset(self):
        return Item_refsQuerySet(self.model, using=self._db)


class Item_refs(Hierarcy):
    child = ForeignKeyProtect(Item, related_name='child')
    parent = ForeignKeyProtect(Item, related_name='parent', blank=True, null=True)

    # def get_parent(self, parent, path_array):
    #     path_array.append(parent.item_name)
    #     self.get_parent(parent.parent)
    #
    # def full_path(self):
    #     path_array = [self.child.item_name]
    #     parent

    props = Item_refsManager.props()

    objects = TreeAuditModelManager()
    objects1 = Item_refsManager()

    def __str__(self):
        return f'\nID={self.id}, child=[{self.child}], parent=[{self.parent}]'

    class Meta:
        verbose_name = 'Item_refs'
        constraints = [
            CheckConstraint(check=~Q(child=F('parent')), name='Item_refs_not_circulate_refs'),
            UniqueConstraint(fields=['child', 'parent'], name='Item_refs_unique_1'),
            UniqueConstraint(fields=['child'], condition=Q(parent=None), name='Item_refs_unique_2'),
        ]
