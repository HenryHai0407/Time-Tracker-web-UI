from flask import Flask, render_template, jsonify, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import pytz

app = Flask(__name__)

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
json_keyfile_path = os.path.join(os.path.dirname(__file__), "time-tracker-project-450421-f3fc3aec2f6a.json")
creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
client = gspread.authorize(creds)

# Open the Google Sheet
SHEET_NAME = "Time_tracker sheet - Yliopistonkatu"
sheet = client.open(SHEET_NAME).sheet1

# Time zone setup (Helsinki)
TIMEZONE = pytz.timezone("Europe/Helsinki")

# Function to format time
def format_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M:%S").strftime("%I:%M %p")
    except ValueError:
        return time_str  # Return as-is if it can't be parsed as time

# Function to convert to Helsinki time zone
def convert_to_hel_time(dt):
    # Ensure dt is naive (no timezone info) before localization
    if dt.tzinfo is not None:
        dt = dt.replace(tzinfo=None)  # Remove any existing timezone info
    utc_time = pytz.utc.localize(dt)  # Localize to UTC first
    hel_time = utc_time.astimezone(TIMEZONE)  # Convert to Helsinki time zone
    return hel_time

@app.route("/")
def index():
    # Fetch data from Google Sheets
    data = sheet.get_all_records()

    # Format the data
    for row in data:
        row['Login'] = format_time(row.get('Login', ''))
        row['Logout'] = format_time(row.get('Logout', ''))
        row['Total working hours'] = row.get('Total working hours', 'N/A')
        row['Employee Name'] = row.get('Employee Name', 'No Name')  
        row['Date'] = row.get('Date', 'No Date')  
        row['Location'] = row.get('Location', 'No Location')  

    return render_template("index.html", data=data)

@app.route("/data")
def get_data():
    # Get the employee name from the query parameter
    employee_name = request.args.get("name", "").strip()

    # Fetch all data from the sheet
    data = sheet.get_all_records()

    # Filter data if employee name is provided
    if employee_name:
        data = [row for row in data if row.get("Employee Name") and employee_name.lower() in row["Employee Name"].lower()]

    # Format the data for the response
    for row in data:
        row['Login'] = format_time(row.get('Login', ''))
        row['Logout'] = format_time(row.get('Logout', ''))
        row['Total working hours'] = row.get('Total working hours', 'N/A')
        row['Employee Name'] = row.get('Employee Name', 'No Name')
        row['Date'] = row.get('Date', 'No Date')
        row['Location'] = row.get('Location', 'No Location')

    return jsonify(data)

@app.route("/update", methods=["POST"])
def update_time():
    data = request.json
    name = data.get("name")
    action = data.get("action")
    location = data.get("location")

    if not name or not action:
        return jsonify({"success": False, "message": "Invalid request"}), 400

    records = sheet.get_all_records()
    row_number = None

    # Find the employee row
    for i, row in enumerate(records, start=2):
        if row.get("Employee Name") == name:
            row_number = i
            break

    if row_number is None:
        return jsonify({"success": False, "message": "Employee not found"}), 404

    # Get current UTC date and time
    now_time_utc = datetime.utcnow().replace(tzinfo=None)  # Remove any existing tzinfo (naive datetime)
    hel_time = convert_to_hel_time(now_time_utc)  # Convert to Helsinki time
    now_time = hel_time.strftime("%H:%M:%S")
    now_date = hel_time.strftime("%d/%m/%Y")

    if action == "Login":
        sheet.update_cell(row_number, 2, now_date)  # Update 'Date'
        sheet.update_cell(row_number, 3, now_time)  # Update 'Login'
        sheet.update_cell(row_number, 5, location)  # Update 'Location'
    elif action == "Logout":
        sheet.update_cell(row_number, 4, now_time)  # Update 'Logout'
        login_time = row.get("Login")

        if login_time:
            fmt = "%H:%M:%S"
            try:
                tdelta = datetime.strptime(now_time, fmt) - datetime.strptime(login_time, fmt)
                total_hours = str(tdelta)[:-3]  # Remove seconds
                sheet.update_cell(row_number, 6, total_hours)  # Update 'Total working hours'
            except ValueError:
                pass  

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
