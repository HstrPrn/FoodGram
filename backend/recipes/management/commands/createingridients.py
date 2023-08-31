import csv
import os
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser
from django.db import IntegrityError

from recipes.models import Ingridient


class Command(BaseCommand):
    help = 'Populate ingridient table in data base with csv file'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-p', '--path', type=str)

    def handle(self, *args: Any, **options: Any) -> None:
        path_to_file = os.path.join(settings.BASE_DIR.parent, options['path'])

        with open(path_to_file) as f:
            rows = csv.DictReader(f, fieldnames=['name', 'measurement_unit'])
            for row in rows:
                try:
                    Ingridient.objects.get_or_create(**row)
                except IntegrityError:
                    print('Ingredient already added')
                    continue
        self.stdout.write(
            self.style.SUCCESS('Successfully created ingridients')
        )

