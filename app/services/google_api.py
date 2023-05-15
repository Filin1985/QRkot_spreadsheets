from aiogoogle import Aiogoogle
# В секретах лежит адрес вашего личного google-аккаунта
from app.core.config import settings

# Константа с форматом строкового представления времени
FORMAT = "%Y/%m/%d %H:%M:%S"
TABLE_NAME = 'Отчет'
SHEET_NAME = 'Рейтинг'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover(
        api_name='sheets',
        api_version='v4'
    )
    spreadsheet_body = {
        'properties': {
            'title': TABLE_NAME,
            'locale': 'ru_RU'
        },
        'sheets': [
            {'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': SHEET_NAME,
                'gridProperties': {
                    'rowCount': 50,
                    'columnCount': 5
                }
            }}
        ]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    await set_user_permissions(
        spreadsheet_id=spreadsheetid,
        wrapper_service=wrapper_services
    )
    table_values = [
        ['Название проекта'],
        ['Время сбора'],
        ['Описание']
    ]
    for project in projects:
        table_values.append([
            project.name,
            str(project.close_date - project.create_date),
            project.description
        ])

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
