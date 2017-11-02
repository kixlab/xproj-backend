from django.core.management.base import BaseCommand
from promises.load import run


class Command(BaseCommand):
    help = 'Imports spatial data from shapefiles into database'

    def handle(self, *args, **options):
        run()
