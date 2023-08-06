import logging

from isc_common.fields.code_field import CodeStrictField
from isc_common.models.base_ref import BaseRefManager, BaseRefQuerySet, BaseRef

logger = logging.getLogger(__name__)


class SectionsQuerySet(BaseRefQuerySet):
    pass


class SectionsManager(BaseRefManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'description': record.description,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return SectionsQuerySet(self.model, using=self._db)


class Sections(BaseRef):
    code = CodeStrictField()
    objects = SectionsManager()

    def __str__(self):
        return f'ID:{self.id}, code: {self.code}, name: {self.name}, description: {self.description}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Разделы в детализации'
