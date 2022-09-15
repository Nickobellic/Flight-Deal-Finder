import requests
from dateutil.relativedelta import relativedelta
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import timedelta
class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.stop_overs = 0

    via_city = []
    deals = []
    service_account_file = 'json file of service'
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    spreadsheet_id = "<spreadsheet-id>"
    credential = service_account.Credentials.from_service_account_file(service_account_file, scopes=scope)
    service = build('sheets', 'v4', credentials=credential)
    sheet = service.spreadsheets()
    iatacode = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range="B2:B").execute()
    lowest_price = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range="C2:C").execute()
    tequila_endpoint = "https://api.tequila.kiwi.com/"
    header = {
        'apikey': 'Tequilla API Key'
    }

    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    min_ret = tomorrow + timedelta(days=7)
    max_ret = tomorrow + timedelta(days=28)
    six_mts = today + relativedelta(months=+6)


    for l in range(len(iatacode['values'])-1): #   len(iatacode['values'])
        try:
            check_flight = {
                'fly_from': 'STN',
                'fly_to': iatacode['values'][l][0],
                'date_from': tomorrow.strftime("%d/%m/%Y"),
                'date_to': six_mts.strftime("%d/%m/%Y"),
                'return_from': min_ret.strftime("%d/%m/%Y"),
                'return_to': max_ret.strftime("%d/%m/%Y"),
                'price_from': 0,
                'max_stopovers': 4,
                'price_to': int(lowest_price['values'][l][0])*50,
                'curr':'INR'
            }
            check = requests.get(url=f"{tequila_endpoint}v2/search", headers=header, params=check_flight).json()
            stops = len(check['data'][0]['route'])//2
            for i in range(0,stops-1):
                via_city.append(f"{check['data'][0]['route'][i]['cityTo']} ")
            price = []

            for i in range(len(check['data'])):
                ticket_price = check['data'][i]['price']
                price.append(ticket_price)
            try:
                best_flight_no = price.index(min(price))
                deals.append(check['data'][best_flight_no])
            except:
                pass

            low_cost = []
            for i in range(len(deals)):
                low_cost.append(deals[i]['price'])
            try:
                perfect_flight_no = low_cost.index(min(low_cost))
                from_city = deals[perfect_flight_no]['cityFrom']
                from_city_code = deals[perfect_flight_no]['cityCodeFrom']
                to_city = deals[perfect_flight_no]['cityTo']
                to_city_code = deals[perfect_flight_no]['cityCodeTo']
                cost = deals[perfect_flight_no]['price']
                from_date = deals[perfect_flight_no]['route'][0]['local_arrival'][:10]
                to_date = deals[perfect_flight_no]['route'][2]['local_arrival'][:10]
            except:
                continue
        except ValueError:
            continue