# Real-Time E-commerce Order and Payment Processing Pipeline using Pub/Sub and Cassandra

## Project Description
This project simulates a real-time data processing pipeline for an e-commerce platform. It processes orders and payments, demonstrating the use of distributed systems and scalable technologies. Here's what happens in this pipeline:

1. **Data Generation**:
   - Mock order and payment data are generated using Python scripts (`order_producer.py` and `payment_producer.py`).
   - These data are published to **Google Cloud Pub/Sub topics**: `orders_data` and `payments_data`.

2. **Data Consumption**:
   - **Order Consumer**: Subscribes to the `orders_data` topic, processes the data, and inserts it into a Cassandra database.
   - **Payment Consumer**: Subscribes to the `payments_data` topic, matches payments with existing orders, and updates the database.

3. **Database Operations**:
   - Data is stored in a Cassandra database as facts in the `orders_payments_facts` table.
   - Each entry in the table captures detailed information about an order and its corresponding payment, creating a single source of truth for analytics.

4. **Dead Letter Queue (DLQ)**:
   - If a payment message doesn't match an existing order in the database, it is sent to a **Dead Letter Queue (DLQ)**.
   - A separate DLQ consumer (`dlq_consumer.py`) handles these unmatched messages for debugging or reprocessing.

5. **Real-World Application**:
   - Such a pipeline can be used in real-world e-commerce platforms to handle millions of orders and payments in real time.
   - The pipeline ensures scalability, fault tolerance, and real-time data availability for analytics or business intelligence.

---

## Features
1. **Producers**:
   - Generate and publish real-time data for orders and payments to Pub/Sub topics.
2. **Consumers**:
   - Process Pub/Sub messages and store the data in a scalable Cassandra database.
3. **Dead Letter Queue**:
   - Handle failed messages gracefully for debugging and reprocessing.
4. **Cassandra Database**:
   - Store both normalized and denormalized data for efficient query performance.

---

## Architecture Overview
The pipeline follows a modular and distributed architecture:
- **Data Producers**:
  - `order_producer.py`: Generates order details and publishes them to the `orders_data` topic.
  - `payment_producer.py`: Generates payment details and publishes them to the `payments_data` topic.
- **Data Consumers**:
  - `order_consumer.py`: Consumes order data, processes it, and inserts it into the Cassandra database.
  - `payment_consumer.py`: Consumes payment data, matches it with orders, and updates the database.
- **Dead Letter Queue**:
  - Handles unmatched payment messages, storing them in the DLQ topic for debugging and resolution.

---


## Instructions

Step 1. **Setup Cassandra**:
Install Docker and run Cassandra using the provided Docker Compose file:
```bash
cd cassandra
docker-compose up -d
```

Set up the database schema by executing the schema.cql file in cqlsh:
```bash
docker exec -it cassandra-db cqlsh
SOURCE 'schema.cql';
```


Step 2: **Set Up Google Pub/Sub**
1. Log in to the Google Cloud Console.
2. Enable the Pub/Sub API in APIs & Services > Library.
3. Create Two Pub/Sub Topics:
    - orders_data
    - payments_data
4. Create Subscriptions for Each Topic:
    - For orders_data: orders_data-sub.
    - For payments_data: payments_data-sub.
Note down the topic names and subscription names for use in the producer and consumer scripts.

Step 3: **Install Dependencies**
```bash
cd producer
pip install -r requirements.txt
```

Step 4. **Run Producers:**
```bash
python3 producer/order_producer.py
python3 producer/payment_producer.py
```

Step 5. **Run Consumers:**
```bash
python3 consumer/order_consumer.py
python3 consumer/payment_consumer.py
```

Step 6. **Run dlq Consumer:**
```bash
python3 dlq/dlq_consumer.py
```

Step 7 **Verify Data**
Query the Cassandra database to verify that orders and payments are correctly processed and stored:
```bash
SELECT * FROM ecom_store.orders_payments_facts;
```
