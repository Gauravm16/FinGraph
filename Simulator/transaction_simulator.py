
import csv
import json
import time
from pathlib import Path
from kafka import KafkaProducer

PROJECT_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = (
    PROJECT_DIR
    / "data"
    / "100vertices-10Kedges"
    / "100vertices-10Kedges"
    / "transactions.csv"
)

KAFKA_TOPIC = "fin_transactions"
KAFKA_SERVER = "localhost:9092"
DELAY_SECONDS = 1


def simulate_transactions():

    if not CSV_FILE.exists():
        print(f"Dataset not found: {CSV_FILE}")
        return

    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_SERVER],
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        key_serializer=lambda key: str(key).encode("utf-8")
    )

    print("FinGraph Kafka Producer started.")
    print(f"Reading: {CSV_FILE}")
    print(f"Sending transactions to: {KAFKA_TOPIC}")
    print("Press Ctrl+C to stop.\n")

    sent_count = 0

    try:
        with CSV_FILE.open(
            "r", newline="", encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                transaction = {
                    "transaction_id": int(row["TX_ID"]),
                    "sender_account": int(row["SENDER_ACCOUNT_ID"]),
                    "receiver_account": int(row["RECEIVER_ACCOUNT_ID"]),
                    "transaction_type": row["TX_TYPE"],
                    "amount": float(row["TX_AMOUNT"]),
                    "timestamp": int(row["TIMESTAMP"]),
                    "is_fraud": row["IS_FRAUD"].strip().lower()
                    in ("true", "1", "yes"),
                    "alert_id": row["ALERT_ID"],
                }

                producer.send(
                    KAFKA_TOPIC,
                    key=transaction["transaction_id"],
                    value=transaction
                )

                sent_count += 1

                print(
                    f"Sent transaction {transaction['transaction_id']} "
                    f"| Amount: {transaction['amount']}"
                )

                time.sleep(DELAY_SECONDS)

    except KeyboardInterrupt:
        print("\nSimulator stopped by user.")

    finally:
        producer.flush()
        producer.close()

        print(f"\nTotal transactions sent: {sent_count}")
        print("Kafka producer closed.")


if __name__ == "__main__":
    simulate_transactions()
