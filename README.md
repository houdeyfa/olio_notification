# olio_notification
Get an email when your favourite shop is available in olio

### Usage

```
pip install requirements.txt
python send_notif_api.py
```

First make sure you have done the instructions below (Gmail and OLIO)

### Gmail activation

Please create an account [here](https://cloud.google.com/)

Create a project and enable Gmail API [here](https://console.cloud.google.com/apis/dashboard)

Create a credential [Oauth](https://console.cloud.google.com/apis/credentials)


On the creds dashboard, click on the download button

Rename the file into ``credentials.json`` and put it in the project's directory

On the first run, it will take you to the google auth page and you have to accept the app to access your Gmail account

Finally, create a file ``email_sender.txt`` where you will have your email address ``you@eample.com``
and a file ``email_list.txt`` with all the emails you want to share as well.
### OLIO setup

Please make sure you have an account [in OLIO](https://volunteers.olioex.com/register)


Create a credential [Oauth](https://console.cloud.google.com/apis/credentials)


Finally, create a file ``olio_user.txt`` where you will have your email address ``you@eample.com`` as the one in your OLIO account add beneath it, you need your password:

```commandline
OLIO_EMAIL_ADDRESS
OLIO_PASS
```