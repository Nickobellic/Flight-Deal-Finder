from flight_search import FlightSearch
from twilio.rest import Client
import smtplib
from googleapiclient.discovery import build
from google.oauth2 import service_account

class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    fc = FlightSearch()
    TWILIO_KEY = "<Twilio Key>"
    SID = "<ID of Twilio>"
    AUTH = "<Twilio Authentication ID>"
    client = Client(SID, AUTH)
    try:
        if fc.stops == 1:
            message = f"Only ₹.{fc.cost} to fly from {fc.from_city}-{fc.from_city_code} to {fc.to_city}-{fc.to_city_code}, from {fc.from_date} to {fc.to_date}."
            sms = client.messages.create(body=f"{message}",
                                         from_='<phone_number>', to='<phone_number>')
        else:
            message = f"Only ₹.{fc.cost} to fly from {fc.from_city}-{fc.from_city_code} to {fc.to_city}-{fc.to_city_code}, from {fc.from_date} to {fc.to_date} with {fc.stops-1} stopovers, {fc.via_city}."
            sms = client.messages.create(body=f"{message}",
                                         from_='<phone_number>', to='<phone_number>')
    except:
        pass

    def create_emails(self):
        fc = FlightSearch()
        url = f"https://www.google.co.uk/flights?hl=en#flt={fc.from_city_code}.{fc.to_city_code}.{fc.from_date}*{fc.to_city_code}.{fc.from_city}.{fc.to_date}"
        if fc.stops == 1:
            message = f"Only ₹.{fc.cost} to fly from {fc.from_city}-{fc.from_city_code} to {fc.to_city}-{fc.to_city_code}, from {fc.from_date} to {fc.to_date}."
        else:
            message = f"Only ₹.{fc.cost} to fly from {fc.from_city}-{fc.from_city_code} to {fc.to_city}-{fc.to_city_code}, from {fc.from_date} to {fc.to_date} with {fc.stops-1} stopovers, {fc.via_city}."
        service_account_file = '<service file>'
        scope = ['https://www.googleapis.com/auth/spreadsheets']
        spreadsheet_id = "<spreadsheet id>"
        credential = service_account.Credentials.from_service_account_file(service_account_file, scopes=scope)
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range="users!C1:C").execute()


        my_email = "<your email>"
        passw = "<your password>"
        smtp = smtplib.SMTP("smtp.gmail.com")
        smtp.starttls()
        smtp.login(user=my_email, password=passw)
        for i in range(1,len(result['values'])):
            message = f"Subject:Flight Deal Found\n\n{message}\n{url}"
            smtp.sendmail(from_addr=my_email, to_addrs=result['values'][i][0], msg=message.encode('utf-8'))
        smtp.close()