from django.core.management.base import BaseCommand
from promises.crawl import get_budget_programs
import datetime


class Command(BaseCommand):
    help = 'Crawls budget data from third-party APIs'

    def add_arguments(self, parser):
        parser.add_argument('--year',
            nargs='?',
            type=int,
            default=datetime.datetime.now().year,
            help='Choose which fiscal year to crawl. Defaults to current year.',
        )

    def handle(self, *args, **options):
        get_budget_programs(options['year'])
