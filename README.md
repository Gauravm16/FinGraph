# FinGraph — Real-Time Financial Transaction Fraud Analytics

## 1. Project Overview

FinGraph is a graph-based financial transaction analytics project that combines **Neo4j, Apache Kafka, and Apache Flink** to analyse financial transaction networks and process simulated transaction streams.

The project represents financial accounts as graph nodes and transactions as directed relationships, enabling the exploration of transaction flows, suspicious connections, and fraud-labelled activity.

In addition to static graph analysis, FinGraph implements a streaming pipeline in which a Python transaction simulator publishes transaction events to Kafka, Apache Flink consumes and processes those events, and Neo4j stores the resulting graph relationships.

## 2. Project Objectives

- Model financial accounts and transactions using a graph database.
- Analyse fraud-labelled transactions using Cypher queries.
- Explore multi-hop transaction paths and account connections.
- Implement a simulated real-time transaction ingestion pipeline.
- Integrate Apache Kafka and Apache Flink with Neo4j.
- Verify successful streaming ingestion into the graph database.
- Evaluate preliminary graph query and transaction ingestion performance.

## 3. Dataset

FinGraph uses a synthetic financial transaction dataset from **IBM AMLSim**.

The dataset includes account information, transaction records, transaction amounts and types, timestamps, fraud-related labels, and alert information.

The dataset is synthetic and intended for research, development, and experimentation.

### Verified Dataset Statistics

| Metric | Result |
|---|---:|
| Total accounts | 100 |
| Total transaction relationships | 17,144 |
| Fraud-labelled transactions | 18 |
| Successfully streamed transactions | 44 |

The 44 streamed transactions were verified in Neo4j using the `stream_processed` relationship property.

Because the streaming pipeline uses Cypher `MERGE`, replayed transactions can update existing relationships without increasing the total relationship count.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Transaction simulation and Kafka event production |
| Apache Kafka | Transaction event streaming and messaging |
| Apache Flink | Stream processing and transaction ingestion |
| Java | Flink streaming application and Neo4j sink |
| Apache Maven | Java dependency management and application packaging |
| Neo4j | Graph database and transaction relationship storage |
| Cypher | Graph queries and fraud analysis |
| Docker / Docker Compose | Containerized Kafka and Flink services |
| Gson | JSON transaction parsing |
| Git / GitHub | Version control and project hosting |
| VS Code | Development environment |

## 5. System Architecture

```text
          Synthetic AMLSim Dataset
                    |
                    v
        Python Transaction Simulator
                    |
                    v
              Apache Kafka
          (fin_transactions)
                    |
                    v
               Apache Flink
         (Java Streaming Application)
                    |
                    v
            Neo4j Transaction Sink
                    |
                    v
              Neo4j Database
                    |
                    v
          Cypher Fraud Analysis
```

### Pipeline Components

**Python Transaction Simulator**

Reads transaction records from the source dataset and publishes JSON messages to the Kafka topic `fin_transactions`.

**Apache Kafka**

Acts as the messaging layer between the transaction simulator and the streaming application.

**Apache Flink**

Consumes transaction events from Kafka and processes them through a Java streaming job.

**Neo4j Transaction Sink**

Parses incoming JSON events, matches the corresponding sender and receiver accounts, and creates or updates `TRANSFERRED_TO` relationships in Neo4j.

**Neo4j Graph Database**

Stores the account network and transaction relationships for further graph-based analysis.

## 6. Graph Data Model

### Account Nodes

Each financial account is represented as an `Account` node, identified by its `ACCOUNT_ID`.

Account information may include customer identifiers, balances, country, account type, and other available source attributes.

### Transaction Relationships

Transactions are represented as directed relationships:

```cypher
(sender:Account)-[:TRANSFERRED_TO]->(receiver:Account)
```

Relationship properties include:

- `tx_id` — Transaction identifier
- `amount` — Transaction amount
- `tx_type` — Transaction type
- `timestamp` — Transaction timestamp
- `is_fraud` — Dataset fraud label
- `alert_id` — Associated alert identifier
- `stream_processed` — Indicates that the transaction was processed by the Flink pipeline

The `stream_processed` property is added during streaming ingestion to support verification.

## 7. Implementation

### 7.1 Data Import and Graph Construction

- Inspected the source CSV files.
- Imported account records into Neo4j.
- Created directed transaction relationships.
- Verified the graph against the source dataset.
- Used Cypher `MERGE` to avoid creating duplicate relationships when importing the same transactions.

### 7.2 Fraud Analysis

Implemented Cypher queries to:

- Count accounts and transaction relationships.
- Identify fraud-labelled transactions.
- Rank accounts by flagged outgoing transactions.
- Calculate amounts associated with flagged transfers.
- Visualize fraud-labelled transaction connections.
- Explore multi-hop transaction paths.

Fraud analysis uses the labels already provided in the synthetic dataset. The project does not implement an independently trained fraud prediction model.

### 7.3 Real-Time Streaming Implementation

Implemented the following pipeline:

1. A Python simulator reads transaction records from the dataset.
2. Transactions are serialized into JSON messages.
3. Messages are published to the Kafka topic `fin_transactions`.
4. A Java-based Apache Flink job consumes the Kafka stream.
5. Gson parses the incoming transaction messages.
6. The Neo4j Java Driver writes the transactions to Neo4j.
7. Cypher `MERGE` creates or updates the corresponding transaction relationships.
8. The `stream_processed` property marks relationships processed through the streaming pipeline.

### 7.4 Streaming Verification

The Flink application was successfully deployed and reached the `RUNNING` state.

The following Cypher query was used to verify streaming ingestion:

```cypher
MATCH ()-[t:TRANSFERRED_TO]->()
WHERE t.stream_processed = true
RETURN count(t) AS streamed_transactions;
```

**Verified result: 44 streamed transactions.**

This confirms successful end-to-end processing from Kafka through Flink into Neo4j.

The result represents a functional integration test, not a sustained throughput or latency benchmark.

## 8. Performance Evaluation

### 8.1 Graph Query Performance

A three-hop transaction traversal was executed to evaluate preliminary graph query performance.

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

All four repeat executions completed below the target in the tested environment.

These observations are exploratory and should not be interpreted as production-scale performance guarantees.

### 8.2 Single-Record Ingestion Performance

Two preliminary ingestion tests were conducted:

| Test | Completion Time |
|---|---:|
| CSV processing using `MERGE` | 640 ms |
| New relationship creation using `CREATE` | 124 ms |

**Performance target:** Less than 1 second.

Both tests completed below the target.

These tests measured individual operations and are separate from the Kafka–Flink streaming implementation.

## 9. Project Structure

```text
FinGraph/
|
├── cypher/
│   ├── 01_import_accounts.cypher
│   ├── 02_import_transactions.cypher
│   └── 03_fraud_analysis.cypher
|
├── data/
│   └── 100vertices-10Kedges/
|
├── simulator/
│   └── transaction_simulator.py
|
├── kafka/
│   └── compose.yaml
|
├── flink/
│   ├── pom.xml
│   └── src/main/java/com/fingraph/
│       ├── FinGraphStreamingJob.java
│       └── Neo4jTransactionSink.java
|
├── README.md
└── .gitignore
```

The synthetic dataset is maintained locally and excluded from Git tracking.

Generated Maven build artifacts and sensitive credentials should also be excluded from version control.

## 10. Running the Streaming Pipeline

### Prerequisites

- Python with the Kafka producer dependency
- Docker Desktop
- Neo4j Desktop with a running database instance
- Java 17
- Apache Maven

### Start Kafka and Flink

From the project root:

```powershell
$env:NEO4J_PASSWORD = Read-Host "Enter Neo4j password"

docker compose -f .\kafka\compose.yaml up -d
```

The Flink dashboard is available at:

`http://localhost:8081`

### Build the Flink Application

```powershell
mvn -f .\flink\pom.xml clean package -DskipTests
```

### Deploy the Streaming Job

```powershell
docker exec fingraph-flink-jobmanager mkdir -p /opt/flink/usrlib

docker cp .\flink\target\fingraph-streaming-2.14.3.jar fingraph-flink-jobmanager:/opt/flink/usrlib/fingraph-streaming.jar

docker exec fingraph-flink-jobmanager flink run -d -c com.fingraph.FinGraphStreamingJob /opt/flink/usrlib/fingraph-streaming.jar
```

The JAR filename corresponds to the currently verified Maven build and may change if the project version is updated.

### Start the Transaction Simulator

```powershell
python .\simulator\transaction_simulator.py
```

The simulator publishes transactions to Kafka for consumption by the Flink application.

### Verify Streaming Ingestion

Run in Neo4j Query:

```cypher
MATCH ()-[t:TRANSFERRED_TO]->()
WHERE t.stream_processed = true
RETURN count(t) AS streamed_transactions;
```

A positive count indicates that transaction relationships have been processed through the streaming pipeline.

**Configuration note:** The Neo4j instance must be accessible at the Bolt address configured in the Java sink. The current local implementation uses `host.docker.internal:7687`.

## 11. Limitations

- The dataset is synthetic rather than real financial transaction data.
- Fraud-labelled transactions are identified using existing dataset labels.
- No machine learning fraud detection model has been developed.
- The transaction simulator replays historical records rather than receiving live banking events.
- Streaming verification covered 44 transactions, not a large-scale load test.
- The implementation has not been benchmarked for sustained throughput, end-to-end latency, or fault tolerance.
- The Neo4j sink performs synchronous database writes and has not been optimized for high-volume production workloads.
- The current implementation is designed for local development and demonstration.

## 12. Future Enhancements

- Develop graph-based suspicious activity detection rules.
- Explore transaction cycles, shared counterparties, and multi-hop fraud patterns.
- Build a monitoring dashboard for financial transactions.
- Implement stream processing metrics and performance monitoring.
- Introduce Flink checkpointing and stronger failure-recovery mechanisms.
- Optimize Neo4j ingestion using batching and asynchronous processing.
- Evaluate scalability with larger transaction datasets.
- Investigate graph-based machine learning techniques for fraud detection.

## 13. Conclusion

FinGraph demonstrates how graph databases and stream processing technologies can be combined for financial transaction analytics.

The project successfully constructs a transaction network containing **100 accounts and 17,144 transaction relationships**, identifies **18 fraud-labelled transactions**, and implements a functional **Python → Kafka → Flink → Neo4j** streaming pipeline.

The successful processing and verification of **44 streamed transactions** demonstrates end-to-end integration between the streaming and graph database components.

FinGraph provides a foundation for further development in graph-based fraud investigation, streaming analytics, and financial transaction monitoring.