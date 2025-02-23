from kafka import KafkaConsumer
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

# Listen for messages
for message in consumer:
    print(f"Received: {message.value}")
