from faker import Faker
import psycopg2
import random
from datetime import timedelta
from dotenv import load_dotenv
import os

print("✅ Starting data generation...")


load_dotenv()
print("📦 Loaded DB_URL:", os.getenv("DB_URL"))

fake = Faker()

import time
from psycopg2 import OperationalError

db_url = os.getenv("DB_URL")

for attempt in range(10):
    try:
        conn = psycopg2.connect(db_url)
        print("✅ Connected to database")
        break
    except OperationalError as e:
        print(f"⏳ Attempt {attempt + 1}: DB not ready yet. Retrying in 3s...")
        time.sleep(3)
else:
    print("❌ Failed to connect to database after 10 attempts.")
    exit(1)

print("conn")
print("📦 Loaded DB_URL:", os.getenv("DB_URL"))
cur = conn.cursor()

print("✅ Starting data generation...")


# Create fake users
for _ in range(100):
    username = fake.user_name()
    cur.execute("INSERT INTO users (username) VALUES (%s)", (username,))

# Create sessions and events
for user_id in range(1, 101):
    for _ in range(random.randint(2, 5)):
        start = fake.date_time_between(start_date='-30d')
        end = start + timedelta(minutes=random.randint(10, 120))
        cur.execute("INSERT INTO sessions (user_id, start_time, end_time, device) VALUES (%s, %s, %s, %s) RETURNING id",
                    (user_id, start, end, random.choice(["PC", "Mobile", "Tablet"])))
        session_id = cur.fetchone()[0]

        for _ in range(random.randint(3, 10)):
            cur.execute("""INSERT INTO events (session_id, event_type, event_time, level, purchase_amount)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (session_id,
                         random.choice(["level_start", "level_complete", "purchase"]),
                         start + timedelta(minutes=random.randint(0, 90)),
                         random.randint(1, 20),
                         random.choice([0, 0, 0, 4.99, 9.99])))
            
print("✅ Data generation complete.")

conn.commit()
cur.close()
conn.close()

print("✅ Data generation complete.")
