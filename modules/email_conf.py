
#libraries for send email
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Send An Email
def send_email(sender_email, receiver_email, subject, html_template, smtp_server, smtp_port, smtp_un,smtp_pw ):
    #sender_email = "abc@hsenidbiz.com"  # Enter your address
    #receiver_email = "iran.u@hsenidbiz.com"  # Enter receiver address

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Turn these into plain/html MIMEText objects
    html = MIMEText(html_template, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(html)
    
    #send email
    #context = ssl.create_default_context()
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.verify_mode = ssl.CERT_NONE
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(smtp_un, smtp_pw)
        reply = server.sendmail(sender_email, receiver_email, message.as_string())
    return reply
