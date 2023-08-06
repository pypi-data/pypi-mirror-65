import logging

from django.core.management import BaseCommand
from django.db import transaction
from tqdm import tqdm

from kaf_pas.ckk.models.item import Item

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Заполнение поля 'Подтвержден' "

    def handle(self, *args, **options):
        logger.info(self.help)

        query = Item.objects.filter(props=~Item.props.confirmed)
        self.pbar = tqdm(total=query.count())

        with transaction.atomic():
            for item in query:
                item.props |= Item.props.confirmed
                item.save()
                self.pbar.update()

        self.pbar.close()
