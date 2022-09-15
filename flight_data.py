from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests

class FlightData:
    #This class is responsible for structuring the flight data.
    service_account_file = 'hello.json'
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    spreadsheet_id = "<spreadsheet id>"
    credential = service_account.Credentials.from_service_account_file(service_account_file, scopes=scope)
    service = build('sheets', 'v4', credentials=credential)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range="A2:A").execute()
    iata = []
    tequila_endpoint = "https://api.tequila.kiwi.com/"
    header = {
        'apikey': 'Tequilla API Key'
    }
    for i in range(0,9):
         # sheety = requests.get(url=f'{sheety_endpoint}/{i}', headers=sheety_auth).json()
         param = {
             'location_types': 'airport',
             'term': str(result['values'][i]),
             'limit': 10
         }
         t = requests.get(url=f"{tequila_endpoint}locations/query", headers=header, params=param).json()
         iata.append([t['locations'][0]['city']['code']])
    request = sheet.values().update(spreadsheetId=spreadsheet_id, range="B2:B11", valueInputOption='RAW',
                                    body={"range": "B2:B11", "values": iata}).execute()
















































































    # sheety_endpoint = "endpoint"

    #
    # # sheety_auth = {
    # #     'Authorization': 'auth'
    # # }


    #     # d = {
    #     #     'price': {
    #     #         'city': sheety['price']['city'],
    #     #         'iatacode': t['locations'][0]['city']['code'],
    #     #         'lowestPrice': sheety['price']['lowestPrice'],
    #     #         'id': i
    #     #     }
    #     # }
    #     # iata_update = requests.put(url=f"{sheety_endpoint}/{i}", headers=sheety_auth, json=d)
    #     # print(sheety)


