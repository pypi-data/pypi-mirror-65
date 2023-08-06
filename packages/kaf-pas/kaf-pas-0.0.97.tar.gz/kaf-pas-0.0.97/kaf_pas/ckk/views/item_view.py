import logging

from django.conf import settings
from django.db import transaction
from django.forms import model_to_dict
from django.shortcuts import redirect

from isc_common import delAttr, setAttr, Stack
from isc_common.common.mat_views import create_tmp_table
from isc_common.http.DSRequest import DSRequest
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException, JsonWSResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.ckk.models.combineItems import CombineItems
from kaf_pas.ckk.models.copyItems import CopyItems
from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.item_line import Item_line
from kaf_pas.ckk.models.item_operations_view import Item_operations_view, Item_operations_viewManager
from kaf_pas.ckk.models.item_refs import Item_refs
from kaf_pas.ckk.models.item_view import Item_view, Item_viewManager
from kaf_pas.system.models.contants import Contants

logger = logging.getLogger(__name__)

item_top_level, _ = Contants.objects.update_or_create(code='top_level', defaults=dict(name='Вершины товарных позиций'))
audo_top_level = Contants.objects.update_or_create(code='audo_top_level', defaults=dict(parent=item_top_level, name='Автоматически сгененрированный состав изделий'))[0].value
typed_top_level = Contants.objects.update_or_create(code='typed_top_level', defaults=dict(parent=item_top_level, name='Типовые кузова'))[0].value
not_typed_top_level = Contants.objects.update_or_create(code='not_typed_top_level', defaults=dict(parent=item_top_level, name='Не типовые кузова'))[0].value
lotsman_top_level = Contants.objects.update_or_create(code='lotsman_top_level', defaults=dict(parent=item_top_level, name='Импорт из Лоцмана'))[0].value


def get_excl():
    excluded = []
    try:
        # excluded = [int(item.value) for item in Contants.objects.filter(code__in=['audo_top_level'])]
        excluded = []
    except:
        pass
    return excluded


def Item_view_query():
    # Item_view._meta.db_table = 'ckk_item_mview'
    query = Item_view.objects.exclude(id__in=get_excl())
    return query


@JsonResponseWithException()
def Item_view_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Item_view_query().
                get_range_rows1(
                request=request,
                function=Item_viewManager.getRecord,
                distinct_field_names=('id',)
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException(printing=False)
def Item_view_Fetch1(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Item_operations_view.objects.
                exclude(id__in=[int(item.value) for item in Contants.objects.filter(code__in=['audo_top_level'])]).
                get_range_rows1(request=request, function=Item_operations_viewManager.getRecord, distinct_field_names=('id',)),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException(printing=False)
def Item_view_Fetch2(request):
    from kaf_pas.production.models.ready_2_launch_detail import Ready_2_launch_detail

    _request = DSRequest(request=request)

    data = _request.get_data()

    with transaction.atomic():
        ready_2_launch_detail = Ready_2_launch_detail.objects.get(id=data.get('id'))
        tmp_table_name = f'ready_2_launch_detail_tmp_table'
        create_tmp_table(
            on_commit=None,
            drop=False,
            sql_str=f'''SELECT
                                       t."isFolder",
                                       t."STMP_1_id",
                                       t."STMP_2_id",
                                       t.deliting,
                                       t.document__file_document,
                                       t.document_id,
                                       t.editing,
                                       t.id,
                                       t.lastmodified,
                                       t.parent_id,
                                       t.props,
                                       t.qty_operations,
                                       t.refs_id,
                                       t.refs_props,
                                       t.relevant,
                                       t.section,
                                       t.version,
                                       t.where_from
                                FROM production_ready_2_launch_detail s
                                         CROSS JOIN LATERAL
                                    json_to_recordset(s.item_full_name_obj::json) as t(
                                                                                       "deliting" boolean,
                                                                                       "document__file_document" text,
                                                                                       "document_id" bigint,
                                                                                       "editing" boolean,
                                                                                       "id" bigint,
                                                                                       "isFolder" boolean,
                                                                                       "lastmodified" text,
                                                                                       "parent_id" bigint,
                                                                                       "props" bigint,
                                                                                       "qty_operations" int4,
                                                                                       "refs_id" bigint,
                                                                                       "refs_props" bigint,
                                                                                       "relevant" text,
                                                                                       "section" text,
                                                                                       "STMP_1_id" bigint,
                                                                                       "STMP_2_id" bigint,
                                                                                       "version" int4,
                                                                                       "where_from" text
                                                                                        )
                                    where s.id = %s''',
            params=[ready_2_launch_detail.id],
            table_name=tmp_table_name)

        return JsonResponse(
            DSResponse(
                request=request,
                data=Item_operations_view.objects.raw(
                    raw_query=f'select * from {tmp_table_name}',
                    function=Item_operations_viewManager.getRecord),
                status=RPCResponseConstant.statusSuccess).response)


class ItemRef:
    def __init__(self, item_ref):
        self.child = item_ref.child.id
        self.parent = item_ref.parent.id if item_ref.parent != None else item_ref.parent
        self.props = item_ref.props

    def __str__(self):
        return f'child: {self.child}, parent: {self.parent}, props: {self.props}'


class UploadTmpTable:
    cnt = 0
    cnt_fall = 0

    def __init__(self, data):
        self.id = data.get('id')
        self.lotsman_document_id = data.get('lotsman_document_id')
        self.stack = Stack()

    def _rec_item_ref(self, item_ref):
        from kaf_pas.ckk.models.tmp_item_refs import Tmp_Item_refs
        if len(self.stack.find(lambda x: x.child == item_ref.child.id and x.parent == (item_ref.parent.id if item_ref.parent else None) and x.props == item_ref.props)) == 0:
            Tmp_Item_refs.objects.create(child=item_ref.child, parent=item_ref.parent, props=item_ref.props)
            item = ItemRef(item_ref=item_ref)
            # print(f'Record Item ({self.stack.size() + 1}): {item}')
            self.stack.push(item)

    def _rec_perents(self, child, level):
        # print(f'level: {level}')
        for item_refs in Item_refs.objects.filter(child=child):
            self._rec_item_ref(item_ref=item_refs)
            if item_refs.parent != None:
                self._rec_perents(child=item_refs.parent, level=level + 1)
                # print(f'level: {level}')

    def make_tmp(self):
        from kaf_pas.kd.models.uploades_documents import Uploades_documents
        from kaf_pas.ckk.models.tmp_item_operations_view import Tmp_Item_operations_view
        from kaf_pas.kd.models.lotsman_documents_hierarcy import Lotsman_documents_hierarcy

        for uploades_document in Uploades_documents.objects.filter(upload_id=self.id):
            for item in Item.objects.filter(document=uploades_document.document):
                self._rec_perents(child=item, level=1)

            for lotsman_documents_hierarcy in Lotsman_documents_hierarcy.objects.filter(document=uploades_document.document):
                for item in Item.objects.filter(lotsman_document=lotsman_documents_hierarcy):
                    self._rec_perents(child=item, level=1)

        print(f'Cnt: {Tmp_Item_operations_view.objects.count()}')


class UploadDocumentTmpTable(UploadTmpTable):
    def make_tmp(self):
        from kaf_pas.ckk.models.tmp_item_operations_view import Tmp_Item_operations_view
        from kaf_pas.kd.models.lotsman_documents_hierarcy import Lotsman_documents_hierarcy

        if self.lotsman_document_id == None:
            for item in Item.objects.filter(document_id=self.id):
                self._rec_perents(child=item, level=1)

            for lotsman_documents_hierarcy in Lotsman_documents_hierarcy.objects.filter(document_id=self.id):
                for item in Item.objects.filter(lotsman_document=lotsman_documents_hierarcy):
                    self._rec_perents(child=item, level=1)
        else:
            for item in Item.objects.filter(lotsman_document_id=self.lotsman_document_id):
                self._rec_perents(child=item, level=1)

        print(f'Cnt: {Tmp_Item_operations_view.objects.count()}')


@JsonResponseWithException(printing=False)
def Item_view_Fetch3(request):
    from kaf_pas.ckk.models.tmp_item_refs import Tmp_Item_refsManager
    from kaf_pas.ckk.models.tmp_item_operations_view import Tmp_Item_operations_viewManager

    _request = DSRequest(request=request)
    data = _request.get_data()

    if settings.LOCKS.locked(f'Item_view_Fetch3_{data.get("id")}'):
        redirect("http://ya.ru")
    settings.LOCKS.acquire(f'Item_view_Fetch3_{data.get("id")}')
    with transaction.atomic():
        Tmp_Item_refsManager.create()
        Tmp_Item_operations_viewManager.create()

        UploadTmpTable(data).make_tmp()

        settings.LOCKS.release(f'Item_view_Fetch3_{data.get("id")}')
        return JsonResponse(
            DSResponse(
                request=request,
                data=Item_operations_view.objects.raw(
                    raw_query=f'''select * from ckk_tmp_item_operations_view''',
                    function=Tmp_Item_operations_viewManager.getRecord
                ),
                status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException(printing=False)
def Item_view_Fetch4(request):
    from kaf_pas.ckk.models.tmp_item_refs import Tmp_Item_refsManager
    from kaf_pas.ckk.models.tmp_item_operations_view import Tmp_Item_operations_viewManager

    _request = DSRequest(request=request)
    data = _request.get_data()

    if settings.LOCKS.locked(f'Item_view_Fetch4_{data.get("id")}'):
        redirect("http://ya.ru")
    settings.LOCKS.acquire(f'Item_view_Fetch4_{data.get("id")}')
    with transaction.atomic():
        Tmp_Item_refsManager.create()
        Tmp_Item_operations_viewManager.create()

        UploadDocumentTmpTable(data).make_tmp()

        settings.LOCKS.release(f'Item_view_Fetch4_{data.get("id")}')
        return JsonResponse(
            DSResponse(
                request=request,
                data=Item_operations_view.objects.raw(
                    raw_query=f'''select * from ckk_tmp_item_operations_view''',
                    function=Tmp_Item_operations_viewManager.getRecord
                ),
                status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_view_Add(request):
    return JsonResponse(DSResponseAdd(data=Item.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonWSResponseWithException()
def Item_view_Update(request):
    return JsonResponse(DSResponseUpdate(data=Item.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_view_Update1(request):
    return JsonResponse(DSResponseUpdate(data=Item_operations_view.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_view_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Item.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_view_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Item.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_view_Info(request):
    return JsonResponse(DSResponse(request=request, data=Item_view_query().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_view_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Item_view.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException(printing=False)
def copyItems(request):
    return JsonResponse(CopyItems(request).response)


@JsonResponseWithException(printing=False)
def combineItems(request):
    return JsonResponse(CombineItems(request).response)


@JsonResponseWithException()
def Item_view_CopyBlockItems(request):
    _request = DSRequest(request=request)
    source = _request.json.get('source')
    destination = _request.json.get('destination')

    if isinstance(source, dict) and isinstance(destination, dict):
        srecords = source.get('records')
        drecord = destination.get('record')

        if isinstance(srecords, list) and isinstance(drecord, dict):
            with transaction.atomic():
                for srecord in srecords:
                    item_refs, created = Item_refs.objects.get_or_create(parent_id=drecord.get('id'), child_id=srecord.get('child_id'))
                    item_line = Item_line.objects.get(id=srecord.get('id'))
                    dict_item_line = model_to_dict(item_line)
                    delAttr(dict_item_line, 'id')
                    setAttr(dict_item_line, 'parent_id', drecord.get('id'))
                    delAttr(dict_item_line, 'parent')
                    setAttr(dict_item_line, 'child_id', dict_item_line.get('child'))
                    delAttr(dict_item_line, 'child')

                    setAttr(dict_item_line, 'SPC_CLM_FORMAT_id', dict_item_line.get('SPC_CLM_FORMAT'))
                    delAttr(dict_item_line, 'SPC_CLM_FORMAT')
                    setAttr(dict_item_line, 'SPC_CLM_ZONE_id', dict_item_line.get('SPC_CLM_ZONE'))
                    delAttr(dict_item_line, 'SPC_CLM_ZONE')
                    setAttr(dict_item_line, 'SPC_CLM_POS_id', dict_item_line.get('SPC_CLM_POS'))
                    delAttr(dict_item_line, 'SPC_CLM_POS')
                    setAttr(dict_item_line, 'SPC_CLM_MARK_id', dict_item_line.get('SPC_CLM_MARK'))
                    delAttr(dict_item_line, 'SPC_CLM_MARK')
                    setAttr(dict_item_line, 'SPC_CLM_NAME_id', dict_item_line.get('SPC_CLM_NAME'))
                    delAttr(dict_item_line, 'SPC_CLM_NAME')
                    setAttr(dict_item_line, 'SPC_CLM_COUNT_id', dict_item_line.get('SPC_CLM_COUNT'))
                    delAttr(dict_item_line, 'SPC_CLM_COUNT')
                    setAttr(dict_item_line, 'SPC_CLM_NOTE_id', dict_item_line.get('SPC_CLM_NOTE'))
                    delAttr(dict_item_line, 'SPC_CLM_NOTE')
                    setAttr(dict_item_line, 'SPC_CLM_MASSA_id', dict_item_line.get('SPC_CLM_MASSA'))
                    delAttr(dict_item_line, 'SPC_CLM_MASSA')
                    setAttr(dict_item_line, 'SPC_CLM_MATERIAL_id', dict_item_line.get('SPC_CLM_MATERIAL'))
                    delAttr(dict_item_line, 'SPC_CLM_MATERIAL')
                    setAttr(dict_item_line, 'SPC_CLM_USER_id', dict_item_line.get('SPC_CLM_USER'))
                    delAttr(dict_item_line, 'SPC_CLM_USER')
                    setAttr(dict_item_line, 'SPC_CLM_KOD_id', dict_item_line.get('SPC_CLM_KOD'))
                    delAttr(dict_item_line, 'SPC_CLM_KOD')
                    setAttr(dict_item_line, 'SPC_CLM_FACTORY_id', dict_item_line.get('SPC_CLM_FACTORY'))
                    delAttr(dict_item_line, 'SPC_CLM_FACTORY')
                    parent_id = dict_item_line.get('parent_id')
                    delAttr(dict_item_line, 'parent_id')
                    child_id = dict_item_line.get('child_id')
                    delAttr(dict_item_line, 'child_id')
                    item_line, created = Item_line.objects.get_or_create(parent_id=parent_id, child_id=child_id, defaults=dict_item_line)

    return JsonResponse(DSResponse(request=request, status=RPCResponseConstant.statusSuccess).response)
