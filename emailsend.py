import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

# Email server configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'yamini582006@gmail.com'
SENDER_PASSWORD = 'qemg fgtb lxzz ixbg'

# Base URL for phishing links (replace with your ngrok public URL)
TRACKING_URL = 'https://142b-2409-40f4-f-59b2-f5a9-9769-e495-cb32.ngrok-free.app/track-click?email='

# Read recipient list from CSV
recipients = pd.read_csv('email_list.csv')

def send_emails():
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Loop through each recipient
        for _, row in recipients.iterrows():
            redirecting = '&redirect=https://aakashkumar-2005.github.io/Phishing_Awareness_HR/'
            recipient_email = row['Email']
            tracking_link = TRACKING_URL + recipient_email + redirecting

            # Create the email content
            subject = "Urgent: Review and Acknowledge the updated 2025 company policies"
            body = f"""
            <html>
            <body>
                <p>Dear [Employee Name],</p>

                <p>As part of our annual review, we have updated several key company policies for the year 2025. It is mandatory for all employees to review and acknowledge these changes to ensure compliance with the updated guidelines.</p>

                <p>Please click the link below to review the updated policies and confirm your acknowledgment:</p>

                <p><a href="{tracking_link}" style="color: blue; text-decoration: underline;">Review Updated Policies Here</a></p>

                <p>The deadline for acknowledgment is [Insert Deadline]. Failure to acknowledge the updated policies could result in disciplinary actions.</p>

                <p>Best regards,<br>
                [HR Head Name]<br>
                Head of Human Resources<br>
                TVS Mobility</p>
            </body>
            </html>
            """

            # Create the MIME message
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))  # Ensure email body is HTML

            # Send the email
            server.send_message(msg)
            print(f"Email sent to {recipient_email}")

        # Close the server
        server.quit()
        print("All emails sent successfully.")

    except Exception as e:
        print(f"Error: {e}")

# Send the emails
send_emails()
