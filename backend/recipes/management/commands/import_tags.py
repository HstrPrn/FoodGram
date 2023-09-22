import csv
import os
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser
from django.db import IntegrityError

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Populate tags table in data base with csv file'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-f', '--filename', type=str)

    def handle(self, *args: Any, **options: Any) -> None:
        path_to_file = os.path.join(
            settings.BASE_DIR.parent,
            'data/',
            options['filename']
        )

        with open(path_to_file) as f:
            rows = csv.DictReader(f, fieldnames=['name', 'color', 'slug'])
            for row in rows:
                try:
                    Tag.objects.get_or_create(**row)
                except IntegrityError:
                    self.stdout.write(self.style.NOTICE(
                        'Tag already added'
                    ))
                    continue
        self.stdout.write(
            self.style.SUCCESS('Successfully created tags')
        )
