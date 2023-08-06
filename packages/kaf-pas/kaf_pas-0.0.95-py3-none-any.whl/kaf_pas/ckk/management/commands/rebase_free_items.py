import logging

from django.core.management import BaseCommand
from django.db import transaction, connection
from tqdm import tqdm

from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.item_refs import Item_refs
from kaf_pas.ckk.views.item_view import audo_top_level

logger = logging.getLogger(__name__)
logger1 = logging.getLogger(f'{__name__}_1')


class Command(BaseCommand):
    help = "Перенос чертежей в подпапку"

    def handle(self, *args, **options):

        logger.info(self.help)

        def get_sql_str(s='count(*)'):
            return f'''select {s}
                        from (
                                 (select *
                                 from ckk_item)
                                 except
                                 (select *
                                 from ckk_item
                                 where id in (select child_id from ckk_item_refs))
                             ) as a'''

        with connection.cursor() as cursor:
            print('Counting')

            cursor.execute(get_sql_str())
            cnt, = cursor.fetchone()
            print(f'Count: {cnt}')

        with transaction.atomic():
            print('Prepare')
            self.pbar = tqdm(total=cnt)
            for item in Item.objects.raw(get_sql_str(s='*')):
                Item_refs.objects.get_or_create(child=item, parent_id=int(audo_top_level))

                if self.pbar:
                    self.pbar.update()

        if self.pbar:
            self.pbar.close()
