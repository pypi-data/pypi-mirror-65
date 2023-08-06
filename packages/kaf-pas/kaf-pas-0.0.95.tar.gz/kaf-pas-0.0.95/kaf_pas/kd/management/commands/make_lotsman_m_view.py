import logging

from django.core.management import BaseCommand

from kaf_pas.kd.models.lotsman_documents_hierarcy_ext import Lotsman_documents_hierarcyManagerExt

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Тестирование get_m_view"

    def handle(self, *args, **options):
        logger.info(self.help)

        Lotsman_documents_hierarcyManagerExt(user=2).make_mview()
