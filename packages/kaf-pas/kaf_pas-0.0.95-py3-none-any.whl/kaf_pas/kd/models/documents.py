import logging
import os
from os.path import getsize

from bitfield import BitField
from django.conf import settings
from django.db import transaction
from django.db.models import DateTimeField, TextField, PositiveIntegerField

from isc_common import delAttr, replace_alt_set
from isc_common.common.mat_views import refresh_mat_view, create_tmp_mat_view, drop_mat_view
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsManager, CommonManagetWithLookUpFieldsQuerySet
from isc_common.models.audit import AuditModel
from kaf_pas.ckk.models.attr_type import Attr_type
from kaf_pas.kd.models.pathes import Pathes

logger = logging.getLogger(__name__)


class DocumentQuerySet(CommonManagetWithLookUpFieldsQuerySet):
    pass


class DocumentManager(CommonManagetWithLookUpFieldsManager):
    type_bad = Attr_type.objects.get_attr(code='KD_BAD')

    def get_queryset(self):
        return DocumentQuerySet(self.model, using=self._db)

    @staticmethod
    def get_m_view():
        sql_str = '''SELECT kd.id,
                            kd.editing,
                            kd.deliting,
                            kd.lastmodified,
                            kd.file_document,
                            kd.file_size,
                            kd.file_modification_time,
                            kd.file_access_time,
                            kd.file_change_time,
                            kd.attr_type_id,
                            kd.path_id,
                            kd.props,
                            kd.deleted_at,
                            kd.load_error,
                            ( SELECT kat.id
                                   FROM kd_document_attributes kat
                                     JOIN kd_document_attr_cross dc ON kat.id = dc.attribute_id
                                     RIGHT JOIN ckk_attr_type att ON att.id = kat.attr_type_id
                                  WHERE dc.document_id = kd.id AND att.code::text = 'STMP_1'::text) AS "STMP_1_id",
                            ( SELECT kat.id
                                   FROM kd_document_attributes kat
                                     JOIN kd_document_attr_cross dc ON kat.id = dc.attribute_id
                                     RIGHT JOIN ckk_attr_type att ON att.id = kat.attr_type_id
                                  WHERE dc.document_id = kd.id AND att.code::text = 'STMP_2'::text) AS "STMP_2_id",
                            relevant_column(kd.props::integer) AS relevant
                           FROM kd_documents kd'''

        drop_mat_view(mat_view_name='kd_documents_mview')
        create_tmp_mat_view(sql_str=sql_str, mat_view_name='kd_documents_mview', indexes=['attr_type_id', 'path_id', 'STMP_1_id', 'STMP_2_id'])

    @staticmethod
    def getRecord(record):
        res = {
            "id": record.id,
            "path_id": record.path.id,
            "attr_type_id": record.attr_type.id,
            "attr_type__code": record.attr_type.code,
            "attr_type__name": record.attr_type.name,
            "file_document": record.file_document,
            "file_size": record.file_size,
            "file_modification_time": record.file_modification_time,
            "file_access_time": record.file_access_time,
            "file_change_time": record.file_change_time,
            "lastmodified": record.lastmodified,
            'load_error': f'<pre>{record.relevant}</pre>' if record.relevant else None,
            "editing": record.editing,
            "deliting": record.deliting,
        }
        return res

    def get_ex(self, *args, **kwargs):
        file_name = kwargs.get('file_document')
        file_drive = kwargs.get('file_drive')
        virt_path = kwargs.get('virt_path')
        attr_type = kwargs.get('attr_type')
        delAttr(kwargs, 'file_document')

        if virt_path:
            if virt_path[0:1] == os.sep or virt_path[0:1] == os.altsep:
                virt_path = virt_path[1:]

        if virt_path:
            if file_name.find(virt_path) == -1:
                _file_name = f'{virt_path}{os.sep}{file_name}'.replace(os.altsep, os.sep)
            else:
                _file_name = file_name.replace(os.altsep, os.sep)
        else:
            _file_name = file_name.replace(os.altsep, os.sep)

        for doc in Documents.objects.filter(path=kwargs.get('path'), attr_type=attr_type, props=Documents.props.relevant).exclude(attr_type=self.type_bad):
            real_file = replace_alt_set(f'{file_drive}{os.sep}{file_name}')

            if replace_alt_set(doc.file_document) == replace_alt_set(_file_name):
                real_file_size = getsize(real_file.replace(replace_alt_set(virt_path), '') if virt_path else real_file)

                # real_file_modification_time = datetime.fromtimestamp(getmtime(real_file)).replace(microsecond=0)
                # system_file_modification_time = doc.file_modification_time.replace(microsecond=0)

                # real_file_access_time = datetime.fromtimestamp(getatime(real_file)).replace(microsecond=0)
                # system_file_access_time = doc.file_access_time.replace(microsecond=0)
                #
                # real_file_change_time = datetime.fromtimestamp(getctime(real_file)).replace(microsecond=0)
                # system_file_change_time = doc.file_change_time.replace(microsecond=0)

                if doc.file_size != real_file_size:
                    # logger.debug(f'Неравенство размеров {doc.file_size} != {real_file_size}')
                    return doc, True
                # elif system_file_modification_time != real_file_modification_time:
                #     logger.debug(f'Неравенство file_modification_time {system_file_modification_time} != {real_file_modification_time}')
                #     return doc, True
                # elif system_file_access_time != real_file_access_time:
                #     logger.debug(f'Неравенство file_access_time {system_file_access_time} != {real_file_access_time}')
                #     return doc, True
                # elif system_file_change_time != real_file_change_time:
                #     logger.debug(f'Неравенство file_change_time {system_file_change_time} != {real_file_change_time}')
                #     return doc, True
                else:
                    return doc, False
        return None, None

    def get_ex1(self, *args, **kwargs):
        file_name = kwargs.get('file_document')
        file_drive = kwargs.get('file_drive')
        virt_path = kwargs.get('virt_path')
        attr_type = kwargs.get('attr_type')
        delAttr(kwargs, 'file_document')

        if virt_path:
            if virt_path[0:1] == os.sep or virt_path[0:1] == os.altsep:
                virt_path = virt_path[1:]

        if virt_path:
            if file_name.find(virt_path) == -1:
                _file_name = f'{virt_path}{os.sep}{file_name}'.replace(os.altsep, os.sep)
            else:
                _file_name = file_name.replace(os.altsep, os.sep)
        else:
            _file_name = file_name.replace(os.altsep, os.sep)

        for doc in Documents.objects.filter(path=kwargs.get('path'), attr_type=attr_type).exclude(attr_type=self.type_bad):
            real_file = replace_alt_set(f'{file_drive}{os.sep}{file_name}')

            if replace_alt_set(doc.file_document) == replace_alt_set(_file_name):
                real_file_size = getsize(real_file.replace(replace_alt_set(virt_path), '') if virt_path else real_file)

                # real_file_modification_time = datetime.fromtimestamp(getmtime(real_file)).replace(microsecond=0)
                # system_file_modification_time = doc.file_modification_time.replace(microsecond=0)

                # real_file_access_time = datetime.fromtimestamp(getatime(real_file)).replace(microsecond=0)
                # system_file_access_time = doc.file_access_time.replace(microsecond=0)
                #
                # real_file_change_time = datetime.fromtimestamp(getctime(real_file)).replace(microsecond=0)
                # system_file_change_time = doc.file_change_time.replace(microsecond=0)

                if doc.file_size != real_file_size:
                    # logger.debug(f'Неравенство размеров {doc.file_size} != {real_file_size}')
                    return doc, True
                # elif system_file_modification_time != real_file_modification_time:
                #     logger.debug(f'Неравенство file_modification_time {system_file_modification_time} != {real_file_modification_time}')
                #     return doc, True
                # elif system_file_access_time != real_file_access_time:
                #     logger.debug(f'Неравенство file_access_time {system_file_access_time} != {real_file_access_time}')
                #     return doc, True
                # elif system_file_change_time != real_file_change_time:
                #     logger.debug(f'Неравенство file_change_time {system_file_change_time} != {real_file_change_time}')
                #     return doc, True
                else:
                    # Для импорта из Лоцмана т.к. состоит из многих узлов,  которые закачиваются сами по себе
                    return doc, False
        return None, None

    def updateFromRequest(self, request, removed=None, function=None):
        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)
        data = request.get_data()

        relevant = data.get('relevant')
        props = data.get('props')

        if relevant == 'Актуален':
            props |= Documents.props.relevant
        else:
            props &= ~Documents.props.relevant

        res = super().get(id=data.get('id'))
        res.props = props
        res.save()
        refresh_mat_view('kd_documents_mview')

        return data

    @staticmethod
    def delete(id, user):
        from isc_common.auth.models.user import User
        from kaf_pas.kd.models.document_attr_cross import Document_attr_cross
        from kaf_pas.kd.models.documents_thumb import Documents_thumb
        from kaf_pas.kd.models.documents_thumb10 import Documents_thumb10
        from kaf_pas.kd.models.lotsman_documents_hierarcy import Lotsman_documents_hierarcy
        from kaf_pas.kd.models.lotsman_documents_hierarcy_files import Lotsman_documents_hierarcy_files
        from kaf_pas.kd.models.lotsman_documents_hierarcy_refs import Lotsman_documents_hierarcy_refs
        from kaf_pas.kd.models.uploades_documents import Uploades_documents

        if not isinstance(user, User):
            raise Exception(f'user  must be a User instance.')

        settings.LOCKS.acquire('DocumentManager.delete')
        res = 0
        lotsman_res = 0

        Uploades_documents.objects.filter(document_id=id).delete()
        Documents_thumb.objects.filter(document_id=id).delete()
        Documents_thumb10.objects.filter(document_id=id).delete()
        Document_attr_cross.objects.filter(document_id=id).delete()

        # for item in Item.objects.filter(document_id=id):
        #     ItemManager.delete_recursive(item_id=item.id, user=user)

        Lotsman_documents_hierarcy_files.objects.filter(lotsman_document__document_id=id).delete()

        Documents_thumb.objects.filter(lotsman_document__document_id=id).delete()
        Documents_thumb10.objects.filter(lotsman_document__document_id=id).delete()

        for lotsman_documents_hierarcy in Lotsman_documents_hierarcy.objects.filter(document_id=id):
            Lotsman_documents_hierarcy_refs.objects.filter(child=lotsman_documents_hierarcy).delete()
            Lotsman_documents_hierarcy_refs.objects.filter(parent=lotsman_documents_hierarcy).delete()
            lotsman_documents_hierarcy.delete()
            lotsman_res += 1

        res += Documents.objects.filter(id=id).delete()[0]
        settings.LOCKS.release('DocumentManager.delete')
        return res, lotsman_res

    def deleteFromRequest(self, request):
        from kaf_pas.ckk.models.item import Item
        from kaf_pas.ckk.models.item_image_refs import Item_image_refs
        from kaf_pas.kd.models.documents_thumb import Documents_thumb
        from kaf_pas.kd.models.documents_thumb10 import Documents_thumb10
        from isc_common.auth.models.user import User

        ids = request.GET.getlist('ids')
        request = DSRequest(request=request)
        user_id = request.user_id

        res = 0
        with transaction.atomic():
            for i in range(0, len(ids), 2):
                id = ids[i]
                visibleMode = ids[i + 1]

                if visibleMode != "none":
                    for item in Item.objects.filter(document_id=id):
                        # Item_refs.objects.filter(child=item).soft_delete(visibleMode=visibleMode)
                        # Item_refs.objects.filter(parent=item).soft_delete(visibleMode=visibleMode)

                        # Item_line.objects.filter(child=item).soft_delete(visibleMode=visibleMode)
                        # Item_line.objects.filter(parent=item).soft_delete(visibleMode=visibleMode)

                        Item_image_refs.objects.filter(item=item).soft_delete(visibleMode=visibleMode)

                        Documents_thumb.objects.filter(lotsman_document__document_id=id).soft_delete(visibleMode=visibleMode)
                        Documents_thumb10.objects.filter(lotsman_document__document_id=id).soft_delete(visibleMode=visibleMode)

                        Documents_thumb.objects.filter(document_id=id).soft_delete(visibleMode=visibleMode)
                        Documents_thumb10.objects.filter(document_id=id).soft_delete(visibleMode=visibleMode)

                    Item.objects.filter(document_id=id).soft_delete(visibleMode=visibleMode)
                    res += super().filter(id=id).soft_delete(visibleMode=visibleMode)
                else:
                    res += DocumentManager.delete(id, User.objects.get(id=user_id))
        refresh_mat_view('kd_documents_mview')
        refresh_mat_view('kd_lotsman_documents_hierarcy_mview')
        return res


class Documents(AuditModel):
    path = ForeignKeyProtect(Pathes, verbose_name='Путь к документу')
    attr_type = ForeignKeyProtect(Attr_type, verbose_name='Тип документа')
    file_document = TextField(verbose_name='Полный путь к файлу', db_index=True)
    file_size = PositiveIntegerField(verbose_name='Размер файла')
    file_modification_time = DateTimeField(verbose_name='Дата время поcледнего модификации документа', null=True, blank=True, db_index=True)
    file_access_time = DateTimeField(verbose_name='Дата время поcледнего доступа к документу', null=True, blank=True, db_index=True)
    file_change_time = DateTimeField(verbose_name='Дата время изменнения документа', null=True, blank=True, db_index=True)
    props = BitField(flags=(
        ('relevant', 'Актуальность'),
        ('beenItemed', 'Был внесен в состав изделий'),
    ), default=1, db_index=True)
    load_error = TextField(null=True, blank=True)

    @property
    def file_name(self):
        (_, filename) = os.path.split(self.file_document)
        return filename

    objects = DocumentManager()

    @property
    def is_cdw(self):
        return self.attr_type.code == 'CDW'

    @property
    def is_spw(self):
        return self.attr_type.code == 'CPW'

    @property
    def is_pdf(self):
        dir, file = os.path.split(self.file_document)
        _, ext = os.path.splitext(file)
        if ext.lower() == '.pdf':
            return True
        else:
            return False

    def __str__(self):
        return f"ID: {self.id}, " \
               f"{self.file_document}, " \
               f"attr_type: [{self.attr_type}], " \
               f"file_document: {self.file_document}, " \
               f"file_size: {self.file_size}, " \
               f"file_modification_time: {self.file_modification_time}, " \
               f"file_access_time: {self.file_access_time}, " \
               f"file_change_time: {self.file_change_time}, " \
               f"props: {self.props}, " \
               f"load_error: {self.load_error}"

    class Meta:
        verbose_name = 'Конструкторские документы'
