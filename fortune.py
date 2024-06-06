# This analysis utilised the folowwing Fortune 500 dataset:
# https://www.kaggle.com/code/winston56/2022-fortune-500-data-collection/output

#importing SQL and CSV reader in Python

import sqlite3
import csv

conn = sqlite3.connect('Fortune_500.sqlite')
cur = conn.cursor()

# Creating an SQL table
cur.executescript('''
DROP TABLE IF EXISTS Fortune500data;

CREATE TABLE Fortune500data (
    company TEXT UNIQUE,
    rank INTEGER,
    rank_change INTEGER,
    revenue INTEGER,
    profit INTEGER,
    num_of_employees INTEGER,
    sector TEXT,
    city TEXT,
    state TEXT,
    newcomer TEXT,
    ceo_founder TEXT,
    ceo_woman TEXT,
    profitable TEXT,
    prev_rank INTEGER,
    ceo_name TEXT,
    website TEXT,
    ticker TEXT,
    market_cap INTEGER
);              
''')

# Parsing and inserting select data from Fortune 500 csv file into the SQL table

with open('Fortune_1000.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row if it exists
    for row in csvreader:
        if len(row) < 18: continue
        company = row[0]
        rank = row[1]
        rank_change = row[2]
        revenue = row[3]
        profit = row[4]
        num_of_employees = row[5]
        sector = row[6]
        city = row[7]
        state = row[8]
        newcomer = row[9]
        ceo_founder = row[10]
        ceo_woman = row[11]
        profitable = row[12]
        prev_rank = row[13]
        ceo_name = row[14]
        website = row[15]
        ticker = row[16]
        market_cap = row[17]

        cur.execute('''INSERT OR IGNORE INTO Fortune500data (company, rank, rank_change, revenue, profit, num_of_employees, sector, city, state, newcomer, ceo_founder, ceo_woman, profitable, prev_rank, ceo_name, website, ticker, market_cap) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            (company, rank, rank_change, revenue, profit, num_of_employees, sector, city, state, newcomer, ceo_founder, ceo_woman, profitable, prev_rank, ceo_name, website, ticker, market_cap))

conn.commit()
conn.close()

# Analysis of SQL table in DB Browser

# Find which sectors are most profitable; assign rounded average revenue as "avg_revenue_billions"

SELECT sector, ROUND(AVG(revenue),1) as avg_revenue_billions
FROM Fortune500data
GROUP BY sector
HAVING avg_revenue_billions>=200
;

# What percentage of companies have a female CEO? 
SELECT 
    (SUM(CASE WHEN ceo_woman = 'yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS ceo_women_percentage
FROM 
    Fortune500data
;

# Which technology companies are top of the Fortune 500 list?
SELECT *
FROM Fortune500data
WHERE sector = 'Technology'
GROUP BY company
ORDER BY RANK ASC
;