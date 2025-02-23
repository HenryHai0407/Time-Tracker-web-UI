from kafka import KafkaProducer
import time
import json

# Set up the Kafka producer
producer = KafkaProducer(
    bootstrap_servers = 'localhost:9092', # Adjust if your Kafka server is on a different host or port
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize the message to JSON
)

# Send messages to the 'time_tracker' topic
messages = [
    {'employee_name': 'Hoang Hai', 'login_time': '2025-02-23T10:00:00', 'logout_time': '2025-02-23T18:00:00', 'location': 'YKH'},
    {'employee_name': 'Alice', 'login_time': '2025-02-23T09:00:00', 'logout_time': '2025-02-23T17:00:00', 'location': 'CC'},
    {'employee_name': 'Bob', 'login_time': '2025-02-23T08:30:00', 'logout_time': '2025-02-23T16:30:00', 'location': 'KPI'}
]

for message in messages:
    producer.send('time_tracker', value=message)
    print(f"Sent: {message}")
    time.sleep(3) # Wait for 3 seconds before sending the next message

producer.flush()
print("All messages have been sent.")