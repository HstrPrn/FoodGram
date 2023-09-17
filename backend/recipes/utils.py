import csv
from collections.abc import KeysView
from typing import List

from django.http import HttpResponse


def download_csv(data: List[dict]) -> HttpResponse:
    response: HttpResponse = HttpResponse(content_type='text/csv')
    field_name: KeysView = data[0].keys()
    writer: csv.DictWriter = csv.DictWriter(response, field_name)
    for d in data:
        writer.writerow(d)
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.csv"'
    )
    return response
