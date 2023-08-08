import requests
import json
import os
import smtplib
import urllib3
from email.mime.text import MIMEText
import os
import pandas as pd  # Import pandas library

os.environ["REQUESTS_CA_BUNDLE"] = r"C:\Users\c.bhavya\Downloads\cacert.pem"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# GitHub API settings
GITHUB_TOKEN = "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"
OWNER = "working-sonata"
REPO = "integration-teams"

# Email settings
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SMTP_USERNAME = "c.bhavya@sonata-software.com"
SMTP_PASSWORD = "Varshu@456"
SENDER_EMAIL = "c.bhavya@sonata-software.com"
RECIPIENT_EMAIL = "c.bhavya@sonata-software.com"

# Load last known state from a file
LAST_STATE_FILE = "last_state.json"
last_state = {}
if os.path.exists(LAST_STATE_FILE):
    with open(LAST_STATE_FILE, "r") as f:
        last_state = json.load(f)

# Fetch pull requests from GitHub
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
response = requests.get(f"https://api.github.com/repos/{OWNER}/{REPO}/pulls", headers=headers, verify=False)
pull_requests = response.json()
print(pull_requests)


# Fetch pull requests from GitHub
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
response = requests.get(f"https://api.github.com/repos/{OWNER}/{REPO}/pulls", headers=headers, verify=False)
pull_requests = response.json()
print(pull_requests)

# Compare with last known state and send email notifications
new_pull_requests = []  # To store new pull requests

for pr in pull_requests:
    pr_id = pr["id"]  # Accessing "id" key from the dictionary
    last_updated = last_state.get(str(pr_id), "")

    if pr["state"] == "closed" and pr["updated_at"] != last_updated:
        new_pull_requests.append(pr)  # Store new pull requests

        # Send email notification using SMTP
        # ... (Rest of your email notification code)

        # Update last known state
        last_state[str(pr_id)] = pr["updated_at"]

# Save updated state to a file
with open(LAST_STATE_FILE, "w") as f:
    json.dump(last_state, f)

# Create DataFrame from all pull requests
df = pd.DataFrame(pull_requests)

# Save DataFrame to an Excel file
output_excel_file = "all_pull_requests.xlsx"
df.to_excel(output_excel_file, index=False)

print(f"Saved {len(pull_requests)} pull requests to {output_excel_file}")

# Convert new pull request data to a DataFrame
df = pd.DataFrame(pull_requests)

# Save DataFrame to an Excel file
output_excel_file = "new_pull_requests.xlsx"
df.to_excel(output_excel_file, index=False)

print(f"Saved {len(new_pull_requests)} new pull requests to {output_excel_file}")
