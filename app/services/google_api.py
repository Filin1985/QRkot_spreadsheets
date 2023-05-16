from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle
# В секретах лежит адрес вашего личного google-аккаунта
from app.core.config import settings

# Константа с форматом строкового представления времени
FORMAT = "%Y/%m/%d %H:%M:%S"
TABLE_NAME = 'Отчет от {now_date_time}'
SHEET_NAME = 'Рейтинг'

ROW_NUMBER = 50
COLUMN_NUMBER = 5
BODY = dict(
    properties=dict(
        title=TABLE_NAME.format(
            now_date_time=datetime.now().strftime(FORMAT)
        ),
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=ROW_NUMBER,
            columnCount=COLUMN_NUMBER,
        )
    ))]
)
HEADER = [
    ['Отчет от', datetime.now().strftime(FORMAT)],
    ['Количество по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        spreadsheet_body=None
) -> str:
    if spreadsheet_body is None:
        spreadsheet_body = deepcopy(BODY)
        spreadsheet_body['properties']['title'] = TABLE_NAME.format(
            date=datetime.now().strftime(FORMAT)
        )
    service = await wrapper_services.discover(
        api_name='sheets',
        api_version='v4'
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    header = deepcopy(HEADER)
    header[0][1] = datetime.now().strftime(FORMAT)
    sorted_projects = sorted(
        projects,
        key=lambda project: project.close_date - project.create_date
    )
    table_values = [
        *header,
        *[list(map(str, [
            attr.name, attr.close_date - attr.create_date, attr.description
        ])) for attr in sorted_projects],
    ]
    columns_number = max(map(len, table_values))
    rows_number = len(table_values)
    if columns_number > COLUMN_NUMBER or rows_number > ROW_NUMBER:
        raise ValueError(
            f'Превышен размер таблицы. '
            f'При лимите столбцов {COLUMN_NUMBER}, получено {columns_number}. '
            f'При лимите строк {ROW_NUMBER}, получено {rows_number}. '
        )
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows_number}C{columns_number}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
