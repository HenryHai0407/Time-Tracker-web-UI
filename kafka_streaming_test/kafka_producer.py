from kafka import KafkaProducer
import time

# Set up the Kafka producer
producer = KafkaProducer(
    bootstrap_servers = 'localhost:9092', # Adjust if your Kafka server is on a different host or port
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize the message to JSON
)

# Send messages to the 'time_tracker' topic
while True:
    message = {
        'employee_name': 'Hoang Hai',
        'login_time': '2025-02-23T10:00:00',
        'logout_time': '2025-02-23T18:00:00',
        'location': 'YKH'
    }

    producer.send('time_tracker', value=message)
    print(f"Sent: {message}")

    time.sleep(5) # Wait for 5 seconds before sending the next message