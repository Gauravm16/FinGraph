
package com.fingraph;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.Session;

import java.util.Map;

public class Neo4jTransactionSink extends RichSinkFunction<String> {

    private transient Driver driver;

    @Override
    public void open(Configuration parameters) {
        String password = System.getenv("NEO4J_PASSWORD");

        if (password == null || password.isEmpty()) {
            throw new IllegalStateException("NEO4J_PASSWORD is missing");
        }

        driver = GraphDatabase.driver(
            "bolt://host.docker.internal:7687",
            AuthTokens.basic("neo4j", password)
        );

        driver.verifyConnectivity();
    }

    @Override
    public void invoke(String json, Context context) throws Exception {
        JsonObject tx = JsonParser.parseString(json).getAsJsonObject();

        String cypher =
            "MATCH (sender:Account {ACCOUNT_ID: $sender}) " +
            "MATCH (receiver:Account {ACCOUNT_ID: $receiver}) " +
            "MERGE (sender)-[t:TRANSFERRED_TO {tx_id: $txId}]->(receiver) " +
            "SET t.amount = $amount, " +
            "t.tx_type = $txType, " +
            "t.is_fraud = $isFraud, " +
            "t.timestamp = $timestamp, " +
            "t.alert_id = $alertId, " +
            "t.stream_processed = true";

        Map<String, Object> params = Map.of(
            "sender", tx.get("sender_account").getAsLong(),
            "receiver", tx.get("receiver_account").getAsLong(),
            "txId", tx.get("transaction_id").getAsLong(),
            "amount", tx.get("amount").getAsDouble(),
            "txType", tx.get("transaction_type").getAsString(),
            "isFraud", tx.get("is_fraud").getAsBoolean(),
            "timestamp", tx.get("timestamp").getAsLong(),
            "alertId", tx.get("alert_id").getAsLong()
        );

        try (Session session = driver.session()) {
            session.executeWrite(transaction -> {
                transaction.run(cypher, params).consume();
                return null;
            });
        }
    }

    @Override
    public void close() {
        if (driver != null) {
            driver.close();
        }
    }
}
