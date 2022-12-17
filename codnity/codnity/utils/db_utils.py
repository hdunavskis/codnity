import logging
from django.db import IntegrityError, transaction
from hacker_news.models import Codnity 

logging.basicConfig(level=logging.DEBUG)


class DBUtils:
    @staticmethod
    def save_results(saved_data) -> None:
        flatten = [data for sub in saved_data for data in sub]
        try:
            with transaction.atomic():
                for data in flatten:
                    _, _ = Codnity.objects.update_or_create(
                        title=data.title,
                        defaults={
                            'title':data.title,
                            'link':data.link,
                            'points':data.points,
                            'created':data.created
                            }
                    )
        except IntegrityError as integrity:
            logging.error('Failed to save to db %s', integrity)
