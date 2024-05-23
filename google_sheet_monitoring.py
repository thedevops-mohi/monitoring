import gspread
import ssl
import time
from email.message import EmailMessage
import smtplib
import schedule
from oauth2client.service_account import ServiceAccountCredentials


def cpu_check():

    scopes = {
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    }

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "[secret key file location goes here]]/secret_key.json", scopes=scopes)
    file = gspread.authorize(creds)
    workbook = file.open("CPU-USAGE")
    sheet = workbook.sheet1

    cidc_col_name = sheet.acell('A1').value
    lidc_col_name = sheet.acell('B1').value

    cidc_cpu_usage = int((sheet.acell('A2').value))
    lidc_cpu_usage = int((sheet.acell('B2').value))

    def cidc_send_email():
        email_sender = 'sender email address goes here'
        # email_password = os.environ("EMAIL_PASSWORD")
        email_password = 'email password goes here'
        email_receiver = 'receiver email address goes here'

        subject = f'{cidc_col_name} Vcenter CPU Utilization has reached {cidc_cpu_usage}%'
        body = f"""
            CPU Utilization: {cidc_cpu_usage}
            vCenter: {'vCenter.' + cidc_col_name}
            Environment: {cidc_col_name}
        """

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

    def lidc_send_email():
        email_sender = '[sender email address goes here]]'
        # email_password = os.environ("EMAIL_PASSWORD")
        email_password = 'email password goes here'
        email_receiver = 'receiver email address goes here'

        subject = f'{lidc_col_name} Vcenter CPU Utilization has reached {lidc_cpu_usage}%'
        body = f"""
            CPU Utilization: {lidc_cpu_usage}
            vCenter: {'vCenter.' + lidc_col_name}
            Environment: {lidc_col_name}
        """

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

    if cidc_cpu_usage >= 80:
        cidc_send_email()
        print(f'{cidc_col_name} CPU usage has reached {cidc_cpu_usage}%')
    else:
        print(f'{cidc_col_name} is all good')

    if lidc_cpu_usage >= 80:
        lidc_send_email()
        print(f'{lidc_col_name} CPU usage has reached {lidc_cpu_usage}%')
    else:
        print(f'{lidc_col_name} is all good')


schedule.every(1).minutes.do(cpu_check)
while True:
    schedule.run_pending()
    time.sleep(1)
