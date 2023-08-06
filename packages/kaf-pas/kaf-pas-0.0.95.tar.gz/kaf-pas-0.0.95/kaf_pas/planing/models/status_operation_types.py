import logging

from bitfield import BitField
from django.conf import settings
from django.db import transaction

from isc_common import setAttr, delAttr
from isc_common.bit import TurnBitOn, TurnBitOff
from isc_common.common import blinkString
from isc_common.fields.code_field import CodeField
from isc_common.fields.related import ForeignKeyCascade
from isc_common.http.DSRequest import DSRequest
from isc_common.models.base_ref import BaseRefManager, BaseRefQuerySet, BaseRef
from isc_common.number import DelProps
from kaf_pas.planing.models.operation_types import Operation_types

logger = logging.getLogger(__name__)


class Status_operation_typesQuerySet(BaseRefQuerySet):
    pass


class Status_operation_typesManager(BaseRefManager):

    def updateFromRequest(self, request, removed=None, function=None):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()

        setAttr(_data, 'opertype_id', _data.get('opertype'))
        delAttr(_data, 'opertype')

        disabled = _data.get('disabled')
        blink = _data.get('blink')
        props = _data.get('props', 0)

        delAttr(_data, 'disabled')
        delAttr(_data, 'blink')
        props = TurnBitOn(props, 0) if disabled else TurnBitOff(props, 0)
        props = TurnBitOn(props, 1) if blink else TurnBitOff(props, 1)
        setAttr(_data, 'props', props)

        super().filter(id=_data.get('id')).update(**_data)
        setAttr(data, 'props', props)
        return data

    @staticmethod
    def make_statuses(opertype, status_map):
        res = dict()
        settings.LOCKS.acquire('Status_operation_typesManager.make_statuses')
        with transaction.atomic():
            for key_value in status_map:
                status, _ = Status_operation_types.objects.update_or_create(
                    opertype=opertype,
                    code=key_value.get('code'),
                    defaults=dict(
                        props=key_value.get('props'),
                        name=key_value.get('name'),
                        color=key_value.get('color'),
                        deliting=False,
                        editing=False,
                    ))
                res.setdefault(key_value.get('code'), status)
        settings.LOCKS.release('Status_operation_typesManager.make_statuses')
        return res

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'description': record.description,
            'editing': record.editing,
            'color': record.color,
            'deliting': record.deliting,
            'disabled': record.props.disabled,
            'blink': record.props.blink,
            'props': record.props,
            'opertype': record.opertype.id,
        }
        return DelProps(res)

    def get_queryset(self):
        return Status_operation_typesQuerySet(self.model, using=self._db)


class Status_operation_types(BaseRef):
    opertype = ForeignKeyCascade(Operation_types)
    color = CodeField(null=True, blank=True)

    props = BitField(flags=(
        ('disabled', 'Неактивная запись в гриде'),
        ('blink', 'Мигающее поле в гриде')
    ), default=0, db_index=True)

    objects = Status_operation_typesManager()

    @property
    def wrap_name(self):
        return blinkString(text=self.name, color=self.color, blink=self.props.blink)

    def __str__(self):
        return f"ID:{self.id}, code: {self.code}, name: {self.name}, description: {self.description}, opertype: [{self.opertype}]"

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Статусы запусков'
