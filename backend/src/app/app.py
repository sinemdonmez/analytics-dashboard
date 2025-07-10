from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from dotenv import load_dotenv
import os

from utils.query_filters import build_filters

load_dotenv()

app = Flask(__name__)
CORS(app)

def connect():
    return psycopg2.connect(os.getenv("DB_URL"))

@app.route("/api/active-users")
def active_users():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(DISTINCT user_id)
        FROM sessions
        WHERE start_time > NOW() - INTERVAL '1 day';
    """)
    result = cur.fetchone()[0]
    conn.close()
    return jsonify({"active_users": result})

@app.route("/api/total-purchases")
def total_purchases():
    conn = connect()
    cur = conn.cursor()
    query = """
        SELECT SUM(purchase_amount)
        FROM events
        JOIN sessions ON events.session_id = sessions.id
        WHERE event_type = 'purchase'
    """
    fields = {
        "device": "device = %s",
        "level": "level = %s",
        "start": "event_time >= %s",
        "end": "event_time <= %s"
    }
    filters, values = build_filters(fields)
    if filters:
        query += " AND " + " AND ".join(filters)
    cur.execute(query, values)
    result = cur.fetchone()[0] or 0
    conn.close()
    return jsonify({"total_purchases": float(result)})

@app.route("/api/popular-levels")
def popular_levels():
    conn = connect()
    cur = conn.cursor()
    query = """
        SELECT level, COUNT(*) as play_count
        FROM events
        JOIN sessions ON events.session_id = sessions.id
        WHERE event_type = 'level_complete'
    """
    fields = {
        "device": "device = %s",
        "level": "level = %s",
        "start": "event_time >= %s",
        "end": "event_time <= %s"
    }
    filters, values = build_filters(fields)
    if filters:
        query += " AND " + " AND ".join(filters)
    query += " GROUP BY level ORDER BY play_count DESC LIMIT 5"
    cur.execute(query, values)
    results = cur.fetchall()
    conn.close()
    return jsonify([{"level": row[0], "play_count": row[1]} for row in results])

@app.route("/api/session-lengths")
def session_lengths():
    conn = connect()
    cur = conn.cursor()
    query = """
        SELECT ROUND(AVG(EXTRACT(EPOCH FROM (end_time - start_time)) / 60)::numeric, 2)
        FROM sessions
        WHERE 1=1
    """
    fields = {
        "device": "device = %s",
        "start": "start_time >= %s",
        "end": "end_time <= %s"
    }
    filters, values = build_filters(fields)
    if filters:
        query += " AND " + " AND ".join(filters)
    cur.execute(query, values)
    avg = cur.fetchone()[0]
    conn.close()
    return jsonify({"average_session_minutes": float(avg) if avg is not None else None})

@app.route("/api/daily-revenue")
def daily_revenue():
    conn = connect()
    cur = conn.cursor()
    query = """
        SELECT DATE(event_time) as date, SUM(purchase_amount) as revenue
        FROM events
        JOIN sessions ON events.session_id = sessions.id
        WHERE event_type = 'purchase'
    """
    fields = {
        "device": "device = %s",
        "level": "level = %s",
        "start": "event_time >= %s",
        "end": "event_time <= %s"
    }
    filters, values = build_filters(fields)
    if filters:
        query += " AND " + " AND ".join(filters)
    query += " GROUP BY date ORDER BY date ASC"
    cur.execute(query, values)
    results = cur.fetchall()
    conn.close()
    return jsonify([{"date": str(row[0]), "revenue": float(row[1]) if row[1] else 0.0} for row in results])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
