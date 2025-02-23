Time Tracker Web App

Overview

The Time Tracker Web App is designed to help businesses monitor employee work hours efficiently. Employees can log in and out using a user-friendly web interface, and their work sessions are automatically recorded. The project also incorporates real-time data processing using Apache Kafka and Spark Structured Streaming, ensuring scalability and automation in tracking work hours.

Features

Employee Work Hour Tracking: Employees can log in and out, recording their working hours.

Location Selection: Users can select their work location when logging in.

Google Sheets Integration: Data is stored and managed in Google Sheets.

Automated Data Flow: Airflow orchestrates data movement and transformations.

Flask Web UI: Provides a simple and mobile-friendly web interface.

Real-time Processing: Kafka and Spark Structured Streaming enable real-time data handling.

Cloud Deployment: Hosted on Render for accessibility.

Tech Stack & Tools

Frontend & Backend: Flask (Python), HTML

Database & Storage: Google Sheets (via Google Apps Script)

Data Orchestration: Apache Airflow

Real-time Streaming: Apache Kafka, Spark Structured Streaming

Cloud & Deployment: Render (for hosting)

Project Structure

Time_Tracker_Project/
│-- airflow/            # Airflow DAGs for managing data pipeline
│-- flask_app/          # Flask-based web UI
│-- kafka/              # Kafka setup and configuration
│-- spark_streaming/    # Spark Structured Streaming processing
│-- static/             # Static files (CSS, JS)
│-- templates/          # HTML templates for web UI
│-- README.md           # Project documentation

Installation & Setup

1. Clone the Repository

git clone https://github.com/your-username/time-tracker.git
cd time-tracker

2. Set Up a Virtual Environment

python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Set Up Kafka

Install Apache Kafka and start the Kafka server.

Create a topic for employee login/logout events.

kafka-topics.sh --create --topic time_tracker_topic --bootstrap-server localhost:9092

5. Start Airflow

airflow db init
airflow webserver & airflow scheduler

6. Run Flask Web App

python app.py

7. Run Spark Structured Streaming

spark-submit spark_streaming.py

Future Improvements

Add user authentication for security.

Improve UI with better frontend frameworks.

Extend real-time analytics dashboard.

Author

Hai Nguyen

Feel free to connect or contribute!

