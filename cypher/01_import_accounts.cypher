
LOAD CSV WITH HEADERS FROM 'file:///accounts.csv' AS row
MERGE (a:Account {ACCOUNT_ID: toInteger(row.ACCOUNT_ID)})
SET a.CUSTOMER_ID = row.CUSTOMER_ID,
    a.INIT_BALANCE = toFloat(row.INIT_BALANCE),
    a.COUNTRY = row.COUNTRY,
    a.ACCOUNT_TYPE = row.ACCOUNT_TYPE,
    a.IS_FRAUD = toLower(row.IS_FRAUD) IN ['true', '1', 'yes'];
