from googleapiclient.discovery import build
from google.oauth2 import service_account

print('Welcome to Flight Deal Finder')

f_name = str(input("What is your First Name? : "))
l_name = str(input("What is your Last Name? : "))
email = str(input("What is your Email ID? : "))
re_email = str(input("Enter your Email again for Confirmation : "))

if email != re_email:
  print('Please Try again')

else:
  value = [[f_name, l_name, email]]
  service_account_file = '<json file of service>'
  scope =['https://www.googleapis.com/auth/spreadsheets']
  spreadsheet_id = "<spreadsheet_id>"
  credential = service_account.Credentials.from_service_account_file(service_account_file, scopes=scope)
  service = build('sheets', 'v4', credentials=credential)
  sheet = service.spreadsheets()
  result = sheet.values().get(spreadsheetId=spreadsheet_id,range="users!A1:A").execute()
  s_id = '<new spreadsheet id>'
  request = {
  'majorDimension': 'ROWS',
  'values': value
}

  service.spreadsheets().values().update( spreadsheetId=spreadsheet_id, valueInputOption = 'USER_ENTERED', range = f"users!A{len(result['values'])+1}", body=request).execute()
  print('You are in the Club!')















