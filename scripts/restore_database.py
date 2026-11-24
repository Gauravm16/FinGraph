
import csv
import os
from pathlib import Path
from neo4j import GraphDatabase

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "backup" / "converted"

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.environ["NEO4J_PASSWORD"]
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def read_csv(filename):
    with (DATA / filename).open(
        encoding="utf-8", newline=""
    ) as file:
        return list(csv.DictReader(file))


def restore_accounts(session, rows):
    query = """
    UNWIND $rows AS row
    MERGE (a:Account {ACCOUNT_ID: toInteger(row.ACCOUNT_ID)})
    SET a.ACCOUNT_TYPE = row.ACCOUNT_TYPE,
        a.COUNTRY = row.COUNTRY,
        a.CUSTOMER_ID = row.CUSTOMER_ID,
        a.INIT_BALANCE = toFloat(row.INIT_BALANCE),
        a.IS_FRAUD = toBoolean(row.IS_FRAUD)
    """
    session.run(query, rows=rows).consume()


def restore_transactions(session, rows):
    query = """
    UNWIND $rows AS row
    MATCH (sender:Account {
        ACCOUNT_ID: toInteger(row.sender_account)
    })
    MATCH (receiver:Account {
        ACCOUNT_ID: toInteger(row.receiver_account)
    })
    MERGE (sender)-[t:TRANSFERRED_TO {
        tx_id: toInteger(row.tx_id)
    }]->(receiver)
    SET t.amount = toFloat(row.amount),
        t.alert_id = toInteger(row.alert_id),
        t.is_fraud = toBoolean(row.is_fraud),
        t.stream_processed = toBoolean(row.stream_processed),
        t.timestamp = toInteger(row.timestamp),
        t.tx_type = row.tx_type
    """
    session.run(query, rows=rows).consume()


def main():
    accounts = read_csv("accounts.csv")
    transactions = read_csv("transactions.csv")

    assert len(accounts) == 100
    assert len(transactions) == 17144

    driver = GraphDatabase.driver(
        URI, auth=(USER, PASSWORD)
    )

    try:
        driver.verify_connectivity()

        with driver.session(database=DATABASE) as session:
            existing = session.run(
                "MATCH (n) RETURN count(n) AS total"
            ).single()["total"]

            if existing != 0:
                raise RuntimeError(
                    "Restoration stopped: target database "
                    "is not empty."
                )

            session.run(
                "CREATE CONSTRAINT account_id_unique IF NOT EXISTS "
                "FOR (a:Account) REQUIRE a.ACCOUNT_ID IS UNIQUE"
            ).consume()

            restore_accounts(session, accounts)
            print("Accounts restored:", len(accounts))

            for start in range(0, len(transactions), 500):
                restore_transactions(
                    session, transactions[start:start + 500]
                )

            print("Transactions processed:", len(transactions))

            result = session.run("""
                MATCH (a:Account)
                WITH count(a) AS accounts
                MATCH ()-[t:TRANSFERRED_TO]->()
                RETURN accounts, count(t) AS transactions
            """).single()

            print("Verified accounts:", result["accounts"])
            print("Verified transactions:", result["transactions"])

            if result["accounts"] != 100 or result["transactions"] != 17144:
                raise RuntimeError("Restored counts do not match backup")

            print("RESTORATION SUCCESSFUL")

    finally:
        driver.close()


if __name__ == "__main__":
    main()
