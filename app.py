from flask import Flask, render_template, request, jsonify
from datetime import datetime
import sqlite3
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

def init_db():
    try:
        with sqlite3.connect("dog_log.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          timestamp TEXT,
                          event TEXT)''')
            conn.commit()
        logging.info("Database initialized successfully")
    except sqlite3.Error as e:
        logging.error(f"Database initialization error: {e}")

@app.before_first_request
def initialize():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log_event', methods=['POST'])
def log_event():
    event = request.json.get('event')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        with sqlite3.connect("dog_log.db") as conn:
            cursor = conn.cursor()
            logging.debug(f"Inserting event: {event} at {timestamp}")
            cursor.execute("INSERT INTO logs (timestamp, event) VALUES (?, ?)", (timestamp, event))
            conn.commit()
        logging.info(f"Event logged: {event} at {timestamp}")
        return jsonify({'timestamp': timestamp, 'event': event})
    except sqlite3.Error as e:
        logging.error(f"Error logging event: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_summary')
def get_summary():
    summary = {"Last Out": None, "Last Peed": None, "Last Pooped": None}
    try:
        with sqlite3.connect("dog_log.db") as conn:
            cursor = conn.cursor()
            for event in summary.keys():
                logging.debug(f"Getting last {event}")
                cursor.execute("SELECT timestamp FROM logs WHERE event=? ORDER BY id DESC LIMIT 1", (event,))
                row = cursor.fetchone()
                if row:
                    summary[event] = row[0]
                logging.debug(f"Last {event}: {summary[event]}")
        return jsonify(summary)
    except sqlite3.Error as e:
        logging.error(f"Error getting summary: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_logs')
def get_logs():
    try:
        with sqlite3.connect("dog_log.db") as conn:
            cursor = conn.cursor()
            logging.debug("Getting all logs")
            cursor.execute("SELECT timestamp, event FROM logs ORDER BY id DESC")
            logs = cursor.fetchall()
        logging.debug(f"Retrieved {len(logs)} logs")
        return jsonify(logs)
    except sqlite3.Error as e:
        logging.error(f"Error getting logs: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/test_db')
def test_db():
    try:
        with sqlite3.connect("dog_log.db") as conn:
            cursor = conn.cursor()
            logging.debug("Inserting test data")
            cursor.execute("INSERT INTO logs (timestamp, event) VALUES (?, ?)", ("test_time", "test_event"))
            conn.commit()

            logging.debug("Selecting test data")
            cursor.execute("SELECT * FROM logs")
            data = cursor.fetchall()
            logging.debug(f"Selected data: {data}")
            return jsonify({"data": data})
    except sqlite3.Error as e:
        logging.error(f"Database test error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)