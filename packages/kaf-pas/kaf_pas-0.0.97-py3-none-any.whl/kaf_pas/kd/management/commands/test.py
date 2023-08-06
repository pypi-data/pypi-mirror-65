import logging

from django.core.management import BaseCommand

from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.item_view import Item_view
from kaf_pas.kd.models.documents_ext import DocumentManagerExt

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Тестирование"

    def handle(self, *args, **options):
        logger.info(self.help)

        DocumentManagerExt(logger=logger).make_pdf(document=document, STMP_1_type=STMP_1_type, STMP_2_type=STMP_2_type)
