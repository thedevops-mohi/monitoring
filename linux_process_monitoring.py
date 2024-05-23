import time
from email.message import EmailMessage
from paramiko import SSHClient, AutoAddPolicy
from rich import print, pretty, inspect
import smtplib
import os
import schedule
import ssl
from json import dumps
from httplib2 import Http

pretty.install()
output = {}
server_ip = input('Enter Server FQDN or IP')
username =  input('Enter Username')
password =  input('Enter Password')


def check_key_server_status():
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())

    client.connect(server_ip, username=username, password=password)

    stdin, stdout, stderr = client.exec_command("monit summary | grep 'keyserver-status'")
    output = stdout.read().decode("utf8").split("'")
    result = output[2].lstrip().rstrip().strip()

    if result != 'Status ok':
        print("ok")
    else:
        send_email()
        main()
    print("####################################################################")
    stdin.close()
    stdout.close()
    stderr.close()

    client.close()


def main():
    """Hangouts Chat incoming webhook quickstart."""
    url = 'google chat channel url goes here'
    bot_message = {
        'text': f"""
        Key-server: Status failed 
        VSD IP: {server_ip}
        Environment: PP1
        Lab 
                """}
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    #print(response)


def send_email():
    email_sender = '[sender email address goes here]]'
    # email_password = os.environ("EMAIL_PASSWORD")
    email_password = 'email password goes here'
    email_receiver = 'receiver email address goes here'

    subject = f'Key-server failed on VSD {server_ip}'
    body = f""" 
        Key-server: Status failed 
        VSD IP: {server_ip}
        Environment: PP1
        Lab 
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

schedule.every(10).seconds.do(check_key_server_status)
schedule.every(10).seconds.do(main)
while True:
    schedule.run_pending()
    time.sleep(10)
