import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def send_email(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        receiver_email = body.get("receiver_email")
        subject = body.get("subject")
        body_text = body.get("body_text")

        if not receiver_email or not subject or not body_text:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "receiver_email, subject, and body_text are required"})
            }

        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_pass = os.getenv("SMTP_PASS")

        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body_text, "plain"))

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, receiver_email, msg.as_string())

        return {"statusCode": 200, "body": json.dumps({"message": "Email sent successfully"})}

    except Exception as e:
        print("Error sending email:", str(e))
        return {"statusCode": 500, "body": json.dumps({"error": "Internal Server Error", "details": str(e)})}
