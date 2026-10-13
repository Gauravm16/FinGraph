
LOAD CSV WITH HEADERS FROM 'file:///transactions.csv' AS row
MATCH (sender:Account {
    ACCOUNT_ID: toInteger(row.SENDER_ACCOUNT_ID)
})
MATCH (receiver:Account {
    ACCOUNT_ID: toInteger(row.RECEIVER_ACCOUNT_ID)
})
MERGE (sender)-[t:TRANSFERRED_TO {
    tx_id: toInteger(row.TX_ID)
}]->(receiver)
SET t.amount = toFloat(row.TX_AMOUNT),
    t.tx_type = row.TX_TYPE,
    t.is_fraud = toLower(row.IS_FRAUD) IN ['true', '1', 'yes'],
    t.timestamp = toInteger(row.TIMESTAMP),
    t.alert_id = toInteger(row.ALERT_ID);
