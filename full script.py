import requests
import json
from datetime import datetime, timedelta

def get_access_token(client_id, client_secret, tenant_id):
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"  # OAuth token endpoint
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'resource': 'https://manage.office.com'
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print("Error getting access token:", response.text)
        return None


# Function to retrieve audit log for a single day
def get_audit_log(access_token, tenant_id, start_time, end_time):
    url = f"https://manage.office.com/api/v1.0/{tenant_id}/activity/feed/subscriptions/content?contentType=Audit.SharePoint&startTime={start_time}&endTime={end_time}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error getting audit log:", response.text)
        return None

def get_logs_for_range(client_id, client_secret, tenant_id):
    access_token = get_access_token(client_id, client_secret, tenant_id)
    if not access_token:
        return None, None

    logs = []
    # Hardcoded test values - replace these with recent dates within the last 7 days
    start_time = "2024-01-17T00:00:00.000Z"
    end_time = "2024-01-17T23:45:00.000Z"
    daily_logs = get_audit_log(access_token, tenant_id, start_time, end_time)
    if daily_logs:
        logs.extend(daily_logs)

    return logs, access_token

def fetch_audit_log_data(access_token, content_uri):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(content_uri, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching audit log data:", response.text)
        return None


# Function to save logs to a file
def save_logs_to_file(logs, file_path):
    with open(file_path, 'w') as file:
        json.dump(logs, file)

# Main function to run the entire process
def main():
    client_id = '60099c6a-3056-450c-8dd1-86943746ced5'
    client_secret = '41Q8Q~xZKaZu6Mi.vXgL.r24haTP~9VLuGLCwaQw'
    tenant_id = 'ffec9c21-f95c-4502-aee3-591c93943a6f'
   # start_date = datetime.now() - timedelta(days=7)
  #  end_date = datetime.now()

    logs = get_logs_for_range(client_id, client_secret, tenant_id)
    if logs:
        save_logs_to_file(logs, 'sharepoint_audit_logs.json')
    else:
        print("No logs found for the specified range.")
    logs, access_token = get_logs_for_range(client_id, client_secret, tenant_id)
    for log_entry in logs:
            content_uri = log_entry.get("contentUri")
            if content_uri:
                audit_log_data = fetch_audit_log_data(access_token, content_uri)
                if audit_log_data:
                    # Process or save the audit log data as needed
                    print(audit_log_data)
    else:
         print("No logs found or failed to retrieve access token.")
