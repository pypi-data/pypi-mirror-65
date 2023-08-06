import logging

from django.core.management import BaseCommand
from django.db import transaction

from kaf_pas.ckk.models.tmp_item_operations_view import Tmp_Item_operations_viewManager, Tmp_Item_operations_view
from kaf_pas.ckk.models.tmp_item_refs import Tmp_Item_refsManager
from kaf_pas.ckk.views.item_view import UploadTmpTable

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Тестирование"

    def handle(self, *args, **options):
        logger.info(self.help)

        with transaction.atomic():
            Tmp_Item_refsManager.create()
            Tmp_Item_operations_viewManager.create()

            UploadTmpTable(dict(id=523)).make_tmp()
            print(f'Cnt: {Tmp_Item_operations_view.objects.count()}')
