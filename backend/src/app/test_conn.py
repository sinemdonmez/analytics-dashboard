import psycopg2, os
print("Connecting to", os.getenv("DB_URL"))
conn = psycopg2.connect(os.getenv("DB_URL"))
print("✅ Connected!")