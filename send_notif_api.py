import datetime
from email.mime.text import MIMEText
import base64
import time
import os.path
from googleapiclient import discovery, errors
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from olio_checker import StoreNameChecker

SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://mail.google.com/']
# The user we want to "impersonate"
email_sender_file = open('email_sender.txt', 'r')
USER_EMAIL = email_sender_file.read()

email_list_file = open('email_list.txt', 'r')
emails = [x.strip() for x in email_list_file.readlines()]


olio_user = open('olio_user.txt', 'r')
OLIO_EMAIL = olio_user.readline().strip()
OLIO_PASS = olio_user.readline().strip()



def validationService():
    creds = None
    # The file tokenxxxx.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            print(creds.to_json())
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    service = build('gmail', 'v1', credentials=creds)

    return service


def SendMessage(service, message):
    message = service.users().messages().send(userId="me", body=message).execute()
    return message


def CreateMessage(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_email_to_group(emails, subject, message):
    service = validationService()
    for email in emails:
        email = CreateMessage(USER_EMAIL, email, subject, message)
        SendMessage(service, email)

def main():
    saved_hour = datetime.datetime.now().hour
    saved_hour = saved_hour + saved_hour % 2
    send_email_to_group(emails,'Bot is (re)starting','Bot is (re)starting')
    olio_checker = StoreNameChecker(OLIO_EMAIL, OLIO_PASS, filter_keyword='')
    shop_list = olio_checker.look_up_stores()
    try:

        while True:
            current_hour = datetime.datetime.now().hour
            current_hour = current_hour + current_hour % 2
            if current_hour != saved_hour:
                send_email_to_group(emails, 'Hour report', f"This is just a reminder, next in 2 hours, you just have the following {shop_list}")
                saved_hour = current_hour
            olio_checker.re_login()

            if (olio_checker.check()):
                mess = 'Olio slot(s) are free, please check out!'
                subject = 'Slot(s) available'
                send_email_to_group(emails, subject, mess)
                time.sleep(60*5)

            time.sleep(60)




    except errors.HttpError as err:
        print('\n---------------You have the following error-------------')
        print(err)
        print('---------------You have the following error-------------\n')
    #except Exception as e:
        #print(e)

if __name__ == '__main__':
    main()
