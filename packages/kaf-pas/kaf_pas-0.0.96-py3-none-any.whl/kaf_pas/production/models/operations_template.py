from django.utils.translation import ugettext_lazy as _

import logging

from isc_common.models.base_ref import BaseRef, BaseRefManager, BaseRefQuerySet, BaseRefHierarcy

logger = logging.getLogger(__name__)


class Operations_templateQuerySet(BaseRefQuerySet):
    def delete(self):
        return super().delete()

    def create(self, **kwargs):
        return super().create(**kwargs)

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Operations_templateManager(BaseRefManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'description': record.description,
            'parent': record.parent.id if record.parent else None,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Operations_templateQuerySet(self.model, using=self._db)


class Operations_template(BaseRefHierarcy):
    objects = Operations_templateManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Шаблоны группы операций'
