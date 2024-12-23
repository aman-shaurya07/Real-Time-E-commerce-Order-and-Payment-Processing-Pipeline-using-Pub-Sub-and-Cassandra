import json
from google.cloud import pubsub_v1

project_id = "big-data-projects-411817"
dlq_subscription_name = "dlq_payments_data-sub"
subscription_path = f"projects/{project_id}/subscriptions/{dlq_subscription_name}"

subscriber = pubsub_v1.SubscriberClient()

def process_dlq_message(message):
    print(f"Received DLQ message: {message.data.decode('utf-8')}")
    message.ack()

if __name__ == "__main__":
    future = subscriber.subscribe(subscription_path, callback=process_dlq_message)
    print("Listening for DLQ messages...")
    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()
