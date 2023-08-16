import poplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    print('Received GitHub Webhook Payload:', payload)

    # Check if the event is a pull request action
    if payload and 'pull_request' in payload:
        action = payload['action']  # Action can be 'opened', 'closed', 'synchronize', etc.
        pr_number = payload['pull_request']['number']

        # Implement logic based on the action
        if action in ['closed', 'merged', 'synchronize']:
            # Send a notification using email
            subject = f"GitHub PR {action.capitalize()}: PR-{pr_number}"
            content = f"The pull request with number {pr_number} has been {action}."
            send_email_notification(subject, content)

    return jsonify(success=True), 200

# Function to send email notifications
def send_email_notification(subject, content):
    from_email = 'c.bhavya@sonata-software.com'  # Replace with your actual email
    to_email = 'kcbhavya09@gmail.com'  # Replace with the recipient's email

    pop_server = 'pop.gmail.com'  # Replace with your POP server address
    pop_port = 995  # Use port 995 for POP3 over TLS
    email_user = 'c.bhavya@sonata-software.com'  # Replace with your actual email
    email_password = 'Varshu@456'  # Replace with your email password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)

    msg.attach(MIMEText(content, 'plain'))

    # Connect to the POP server using TLS
    pop_server = poplib.POP3_SSL(pop_server, pop_port)
    pop_server.user(email_user)
    pop_server.pass_(email_password)

    # Send the email using SMTP with TLS
    with smtplib.SMTP('smtp.office365.com', 587) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(email_user, email_password)
        smtp_server.sendmail(from_email, to_email, msg.as_string())

    # Quit the POP connection
    pop_server.quit()

if __name__ == '__main__':
    app.run(debug=True, port=3000)  # Change the port number if needed
