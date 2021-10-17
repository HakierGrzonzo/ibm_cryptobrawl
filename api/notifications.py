import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

port = 465
server_addr = "mail.postale.io"
sender_email = "cos@example.com"
password = ""
context = ssl.create_default_context()
subscribers = [
        "cos@example.com",
        "cos@example.com",
        "cos@example.com"
    ]

def send_finished(how_much_have_i_made, how_much_i_sleep):
    message = """
    Elo mordeczki!

    Zarobiłem {}USD, mam nadzieje że was to zadowala, możecie handlować jak chcecie.

    Zamierzam wrócić o {}

    Z poważaniem

    Algosy
    """.strip().format(how_much_have_i_made, how_much_i_sleep)
    mail = MIMEMultipart("alternative")
    mail['From'] = sender_email
    mail['Subject'] = "Trejdowanie zakończone!" 
    mail.attach(MIMEText(message, 'plain', 'utf-8'))
    with smtplib.SMTP_SSL(server_addr, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, subscribers, mail.as_string().encode('utf8'))

def send_going_to_start(when):
    message = """
    Elo mordeczko!

    Oddawaj hajs bo będę handlował z nim!

    Będę czekał pod twoim domem o {}!

    Z poważaniem

    Algosy
    """.strip().format(when)
    mail = MIMEMultipart("alternative")
    mail['From'] = sender_email
    mail['Subject'] = "Czekam na twój hajs!" 
    mail.attach(MIMEText(message, 'plain', 'utf-8'))
    with smtplib.SMTP_SSL(server_addr, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, subscribers, mail.as_string().encode('utf8'))

if __name__ == "__main__":
    send_finished("TEST", "TEST2")
    send_going_to_start("TEST")
