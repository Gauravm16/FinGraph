
package com.fingraph;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

public class FinGraphStreamingJob {

    public static void main(String[] args) throws Exception {

        // Step 1: Create Flink execution environment
        StreamExecutionEnvironment env =
                StreamExecutionEnvironment.getExecutionEnvironment();

        // Step 2: Connect Flink to Kafka
        KafkaSource<String> source = KafkaSource.<String>builder()
                .setBootstrapServers("kafka:29092")
                .setTopics("fin_transactions")
                .setGroupId("fingraph-flink-consumer")
                .setStartingOffsets(OffsetsInitializer.earliest())
                .setValueOnlyDeserializer(new SimpleStringSchema())
                .build();

        // Step 3: Read transaction messages from Kafka
        DataStream<String> transactions = env.fromSource(
                source,
                WatermarkStrategy.noWatermarks(),
                "Kafka Transaction Source"
        );

        // Step 4: Write transactions to Neo4j
        transactions
                .addSink(new Neo4jTransactionSink())
                .name("Neo4j Transaction Sink");

        // Step 5: Start the streaming job
        env.execute("FinGraph Real-Time Fraud Analytics");
    }
}
