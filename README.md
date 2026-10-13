# FinGraph — Financial Transaction Fraud Analysis

## Overview
FinGraph is a graph-based data analytics project that explores financial transactions and identifies potentially suspicious activity using Neo4j.

## Objectives
- Model financial accounts as nodes and transfers as relationships.
- Analyse transaction patterns using Cypher queries.
- Explore dataset-labelled fraudulent transactions and identify accounts associated with flagged transfers.

## Dataset
Uses the synthetic financial transaction dataset from **IBM AMLSim**. The dataset contains account details, transactions, and fraud labels for analysis.

## Tools
- **Neo4j:** Graph database and transaction analysis.
- **Cypher:** Query language for importing and analysing graph data.
- **CSV:** Source data format.
- **Git and GitHub:** Version control and project documentation.

## Work Completed
- Imported account records as graph nodes.
- Modelled transactions as directed relationships between accounts.
- Checked account and transaction counts against the source data.
- Queried flagged transactions and ranked sender accounts.
- Visualised flagged transfers in the graph.

## Scope and Limitations
This project analyses synthetic, pre-labelled data. Flagged transactions are dataset labels, not predictions from a trained fraud detection model. The current version is a static graph analysis prototype, not a live fraud monitoring system.

## Project Structure
- `cypher/01_import_accounts.cypher` — Imports account records.
- `cypher/02_import_transactions.cypher` — Creates transaction relationships.
- `cypher/03_fraud_analysis.cypher` — Contains analysis queries.
- `data/` — Local dataset files, if present.

## Future Improvements
- Analyse transaction networks and suspicious paths.
- Add graph-based risk indicators.
- Build a dashboard for investigation and reporting.
