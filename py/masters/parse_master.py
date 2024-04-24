import json
import requests
from io import BytesIO
import py.config as cfg
from openpyxl import Workbook


def get_excel(data):
    try:
        excel_byte_stream = BytesIO()
        wb = Workbook()
        ws = wb.active
        headers = ['Title', 'Volume', 'Price']
        ws.append(headers)

        for item in data:
            ws.append([item['market_hash_name'], item['volume'], item['price']])

        wb.save(excel_byte_stream)
        excel_byte_stream.seek(0)

        return excel_byte_stream
    except:
        return None


def get_items():
    r = requests.get(cfg.API_DOTA)

    try:
        json_data = json.loads(r.text)
    except:
        return None

    try:
        success = json_data['success']
    except:
        return None

    if not success:
        return None

    items = json_data['items']

    return items


if __name__ == "__main__":
    pass
