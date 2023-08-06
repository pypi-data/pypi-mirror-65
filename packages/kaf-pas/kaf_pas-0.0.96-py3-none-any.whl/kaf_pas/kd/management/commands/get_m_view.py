import logging

from django.core.management import BaseCommand

from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.item_view import Item_view
from kaf_pas.kd.models.documents import DocumentManager
from kaf_pas.kd.models.documents_ext import DocumentManagerExt

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Тестирование get_m_view"

    def handle(self, *args, **options):
        logger.info(self.help)

        DocumentManager.get_m_view()

