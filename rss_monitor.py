import feedparser
import sqlite3
import time
import os
query = "JohnSmith"
FEED_URLS = ["https://news.google.com/rss/"]

KEYWORDS = ["surrender", "award", "recognized", "stealth"]

DB_PATH = os.path.abspath("rss_mentions.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mentions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    feed_url TEXT,
    title TEXT,
    link TEXT UNIQUE,
    published TEXT,
    matched_keyword TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

for url in FEED_URLS:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        content = f"{entry.get('title','')} {entry.get('summary', '')}".lower()
        print(content)
        for kw in KEYWORDS:
            if kw in content:
                cursor.execute("INSERT OR IGNORE INTO mentions (feed_url, title, link, published, matched_keyword) "
                               "VALUES (?,?,?,?,?)",
                               (
                                   url,
                                   entry.get('title',''),
                                   entry.get('link',''),
                                   entry.get('published',''),
                                   kw
                               )
                               )
                print(f"[MATCH] '{kw}' found in: {entry.get('title','')}")
                break
conn.commit()
conn.close()
print("Scan Complete")
