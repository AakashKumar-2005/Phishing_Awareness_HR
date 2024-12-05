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
TRACKING_URL = 'https://5ad1-2405-201-e006-1075-f99e-7f9d-ccc2-cb66.ngrok-free.app/track-click?email='

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
            recipient_email = row['Email']
            recipient_name = row['Name']  # Read the name from the CSV
            tracking_link = TRACKING_URL + recipient_email 

            # Create the email content
            subject = "Urgent: Review and Acknowledge the Updated 2025 Company Policies"
            body = f"""
            <html>
            <body>
                <p>Dear {recipient_name},</p>

                <p>As part of our annual review, we have updated several key company policies for the year 2025. 
                It is mandatory for all employees to review and acknowledge these changes to ensure compliance with the updated guidelines.</p>

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
