
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "backup"
OUTPUT = BACKUP / "converted"
OUTPUT.mkdir(exist_ok=True)


def parse_properties(value):
    """Convert Neo4j's exported property map to Python values."""
    result = {}

    for line in value.strip().strip("{}").splitlines():
        line = line.strip().rstrip(",")

        if not line:
            continue

        key, raw = line.split(":", 1)
        key, raw = key.strip(), raw.strip()

        if raw.upper() == "TRUE":
            parsed = True
        elif raw.upper() == "FALSE":
            parsed = False
        elif re.fullmatch(r"-?\d+", raw):
            parsed = int(raw)
        elif re.fullmatch(r"-?(?:\d+\.\d*|\.\d+)(?:[eE][+-]?\d+)?", raw):
            parsed = float(raw)
        else:
            parsed = raw

        result[key] = parsed

    return result


def convert_accounts():
    with (BACKUP / "accounts_backup.csv").open(
        encoding="utf-8-sig", newline=""
    ) as file:
        rows = [
            parse_properties(row["account"])
            for row in csv.DictReader(file)
        ]

    columns = sorted({key for row in rows for key in row})
    assert len(rows) == 100

    with (OUTPUT / "accounts.csv").open(
        "w", encoding="utf-8", newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print("Accounts converted:", len(rows))


def convert_transactions():
    rows = []

    for part in range(1, 5):
        path = BACKUP / f"transactions_part{part}.csv"

        with path.open(encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                properties = parse_properties(row["transaction"])

                rows.append({
                    "sender_account": int(row["sender_account"]),
                    "receiver_account": int(row["receiver_account"]),
                    **properties,
                })

    assert len(rows) == 17144

    columns = [
        "sender_account",
        "receiver_account",
        *sorted({
            key
            for row in rows
            for key in row
            if key not in ("sender_account", "receiver_account")
        }),
    ]

    with (OUTPUT / "transactions.csv").open(
        "w", encoding="utf-8", newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print("Transactions converted:", len(rows))


if __name__ == "__main__":
    convert_accounts()
    convert_transactions()
    print("Converted files saved to:", OUTPUT)
