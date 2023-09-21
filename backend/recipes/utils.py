import csv
from collections.abc import KeysView
from typing import List

from django.http import HttpResponse


def download_csv(data: List[dict]) -> HttpResponse:
    """
    Преобразует данные из словаря в csv формат
    и возвращает HttpResponse класс для отправки клиенту.
    """
    response: HttpResponse = HttpResponse(content_type='text/csv')
    response.write(u'\ufeff'.encode('utf8'))
    field_name: KeysView = data[0].keys()
    writer: csv.DictWriter = csv.DictWriter(response, field_name)
    for d in data:
        writer.writerow(d)
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.csv"'
    )
    return response