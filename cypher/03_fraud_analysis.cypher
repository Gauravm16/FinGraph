
/* 1. Count accounts and transfers */
MATCH (a:Account)
WITH count(a) AS total_accounts
MATCH ()-[t:TRANSFERRED_TO]->()
RETURN total_accounts,
       count(t) AS total_transfers,
       sum(CASE WHEN t.is_fraud THEN 1 ELSE 0 END)
           AS flagged_transfers;

/* 2. Rank accounts by flagged outgoing transfers */
MATCH (a:Account)-[t:TRANSFERRED_TO]->()
WHERE t.is_fraud = true
RETURN a.ACCOUNT_ID AS account_id,
       count(t) AS flagged_transfers,
       sum(t.amount) AS flagged_amount
ORDER BY flagged_transfers DESC
LIMIT 10;

/* 3. Visualize flagged transfers */
MATCH (a:Account)-[t:TRANSFERRED_TO]->(b:Account)
WHERE t.is_fraud = true
RETURN a, t, b
LIMIT 50;
