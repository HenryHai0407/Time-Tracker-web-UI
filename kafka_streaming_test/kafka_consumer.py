from kafka import KafkaConsumer
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import json

# Set up the Kafka consumer
consumer = KafkaConsumer(
    'time_tracker',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),  # Deserialize the message from JSON
    auto_offset_reset='earliest', # Start from the earliest message
    enable_auto_commit=True,
    group_id='time_tracker_group' # Consumer group
)

# Function to append data to Google Sheets
def append_to_google_sheet(sheet_id, range_name, values):
    # Load the credentials from the service account key file
    creds = Credentials.from_service_account_file('time-tracker-project-450421-f3fc3aec2f6a.json')
    service = build('sheets','v4', credentials=creds)

    # Prepare the data to be appended
    body = {
        'values': values
    }

    # Call the Sheets API to append the data
    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()

    print(f"{result.get('updates').get('updatedCells')} cells appended.")

# Google Sheets settings (Extract sheet_id from GS URL link + Range Name)
sheet_id = '1qbdOnYGP9fQ9pfuWiWF5q4VdWTXag7pA_Hz-SemJ0zU'
range_name = 'Test_Tracker_Data!A1' 


# Consume messages and append to Google Sheets
# Listen for messages
for message in consumer:
    print(f"Received: {message.value}")

    # Prepare data for Google Sheets
    row = [
        message.value['employee_name'],
        message.value['login_time'],
        message.value['logout_time'],
        message.value['location']
    ]

    # Append data to Google Sheets
    append_to_google_sheet(sheet_id,range_name,[row])