from django.core.management.base import BaseCommand
from promises.load import run


class Command(BaseCommand):
    help = 'Imports spatial data from shapefiles into database'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--shapefile',
            default='/data/voting-districts/areas.shp',
            help='Path to shapefile (on the Docker container)',
        )

    def handle(self, *args, **options):
        run(options['shapefile'])
