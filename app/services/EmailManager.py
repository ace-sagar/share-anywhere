import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailManager():
    def __init__(self) -> None:
        pass
    
    def send_email(self, recipient_email, subject, body):
        # SMTP configuration
        smtp_server = 'sandbox.smtp.mailtrap.io'
        smtp_port = 587
        smtp_user = 'a1b84a21bfcab6'
        smtp_password = '9781b23b81c5bc'

        # Create message container
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable security
        server.login(smtp_user, smtp_password)  # Login with your email and password
        text = msg.as_string()
        server.sendmail(smtp_user, recipient_email, text)  # Send email
        print('Email sent successfully')
        
        server.quit()
