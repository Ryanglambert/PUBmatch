from email.mime.text import MIMEText
from subprocess import Popen, PIPE
import requests
import schedule
import time

def is_pubmatch_up():
    response = requests.get("http://www.pubmatch.co")
    return response.ok

def send_status():
    msg = MIMEText("ALERT: PUBmatch DOWN")
    msg["From"] = "status@pubmatch.co"
    msg["To"] = "ryan.g.lambert@gmail.com"
    msg["Subject"] = "ALERT: PUBmatch is DOWN"
    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
    p.communicate(msg.as_string())

def status_checker():
    if not is_pubmatch_up():
        send_status()

def main():
    schedule.every(45).minutes.do(status_checker)
    while 1:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()


