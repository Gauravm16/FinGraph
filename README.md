# FinGraph — Financial Transaction Fraud Analysis

## 1. Project Overview

FinGraph is a graph-based financial transaction analysis project built using Neo4j. The project explores how graph databases can represent financial transactions and help investigate potentially suspicious activity.

Unlike traditional relational databases, graph databases represent entities as nodes and their connections as relationships. This makes it easier to explore transaction flows and connections between accounts.

## 2. Project Objectives

- Represent financial accounts as graph nodes.
- Represent transactions as directed relationships between accounts.
- Analyse transaction patterns using Cypher queries.
- Identify accounts associated with fraud-labelled transactions.
- Explore multi-hop transaction paths.
- Evaluate basic graph query and transaction ingestion performance.

## 3. Dataset

This project uses the synthetic financial transaction dataset from **IBM AMLSim**.

The dataset contains:
- Account information.
- Financial transaction records.
- Transaction types and amounts.
- Timestamps.
- Fraud-related labels and alert information.

The dataset is synthetic and intended for research and experimentation.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Neo4j | Graph database |
| Cypher | Graph query language |
| CSV | Source data format |
| Git | Version control |
| GitHub | Project repository |
| VS Code | Code editing and project development |

## 5. Graph Data Model

The project uses two main graph components:

**Account Nodes**

Each account is represented as an `Account` node containing properties such as:
- Account ID
- Customer ID
- Initial balance
- Country
- Account type
- Fraud label

**Transaction Relationships**

Each transaction is represented by a directed `TRANSFERRED_TO` relationship connecting a sender account to a receiver account.

Transaction relationships contain properties such as:
- Transaction ID
- Transaction amount
- Transaction type
- Timestamp
- Fraud label
- Alert ID

## 6. Work Completed

### Data Import and Graph Construction

- Inspected the source CSV files.
- Imported account records into Neo4j.
- Created account-to-account transaction relationships.
- Verified imported records against the source dataset.

### Fraud Analysis

Created Cypher queries to:
- Count total accounts and transactions.
- Identify fraud-labelled transactions.
- Rank accounts by flagged outgoing transactions.
- Calculate the total amount associated with flagged transfers.
- Visualise flagged transaction connections.

### Graph Query Performance

Executed a three-hop transaction traversal to explore connected accounts.

| Test | Completion Time |
|---|---:|
| Initial execution | 452 ms |
| PROFILE execution | 80 ms |
| Repeat 1 | 16 ms |
| Repeat 2 | 42 ms |
| Repeat 3 | 13 ms |
| Repeat 4 | 11 ms |
| Median of repeat runs | **14.5 ms** |

**Performance target:** Less than 100 milliseconds.

All four repeat runs completed below the target in the tested environment.

### Transaction Ingestion Performance

Performed two single-record ingestion tests:

| Test | Completion Time |
|---|---:|
| CSV processing using MERGE | 640 ms |
| New relationship creation using CREATE | 124 ms |

**Performance target:** Less than 1 second.

Both tests completed below the target in the observed runs.

These tests used a single CSV record and do not represent a sustained real-time streaming pipeline.

## 7. Dataset Verification

The final verified graph contains:

| Metric | Result |
|---|---:|
| Total accounts | 100 |
| Total transaction relationships | 17,144 |
| Fraud-labelled transactions | 18 |

A temporary test relationship created during ingestion testing was deleted, and the original transaction count was verified again.

## 8. Project Structure

```text
FinGraph/
│
├── cypher/
│   ├── 01_import_accounts.cypher
│   ├── 02_import_transactions.cypher
│   └── 03_fraud_analysis.cypher
│
├── data/
│   └── 100vertices-10Kedges/
│
├── README.md
└── .gitignore
```

The dataset is maintained locally and excluded from Git tracking.

## 9. Current Project Scope and Limitations

The current implementation is a static graph-analysis prototype using synthetic, pre-labelled transaction data.

Fraud-labelled transactions are identified using the labels already present in the dataset. No independent machine learning fraud detection model has been developed.

The ingestion performance tests are single-record tests, not continuous streaming benchmarks.

## 10. Future Work

- Implement a real-time transaction ingestion pipeline.
- Integrate incoming transactions with Neo4j.
- Develop graph-based suspicious transaction analysis.
- Explore multi-hop transaction patterns.
- Build a dashboard for transaction monitoring and analysis.
- Conduct further performance and scalability testing.

## 11. Conclusion

FinGraph establishes a foundation for graph-based financial transaction analysis using Neo4j. The current implementation successfully models accounts and transactions, analyses fraud-labelled activity, visualises transaction connections, and demonstrates promising preliminary query and ingestion performance.

The next phase will focus on developing real-time transaction processing and more advanced suspicious activity analysis.