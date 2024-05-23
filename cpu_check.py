import ssl
import pandas as pd
import time
from email.message import EmailMessage
import smtplib
import schedule

while True:
    schedule.run_pending()
    time.sleep(30)
    sheet_id = '[google sheet id goes here]'
    sheet_name = 'CPU'
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}".format(sheet_id,sheet_name))
    cpu_percentage = df['CIDC'][0]
    print(cpu_percentage)
    environment = df.columns[0]
    print(environment)


def check_cpu():

    if cpu_percentage >= 80:
        send_email()
        print('Admin notified...........')
    else:
        print('*')



def send_email():
    email_sender = '[sender email address goes here]]'
    # email_password = os.environ("EMAIL_PASSWORD")
    email_password = 'email password goes here'
    email_receiver = 'receiver email address goes here'

    subject = f'{environment} Vcenter CPU Utilization has reached 80%'
    body = f"""
        CPU Utilization: {cpu_percentage}
        vCenter: {'vCenter.' + environment}
        Environment: {environment}
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


schedule.every(1).minutes.do(check_cpu)
check_cpu()
