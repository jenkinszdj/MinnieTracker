from flask import Flask, render_template, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("dog_log.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          timestamp TEXT,
                          event TEXT)''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log_event', methods=['POST'])
def log_event():
    event = request.json.get('event')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with sqlite3.connect("dog_log.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (timestamp, event) VALUES (?, ?)", (timestamp, event))
        conn.commit()
    
    return jsonify({'timestamp': timestamp, 'event': event})

@app.route('/get_summary')
def get_summary():
    summary = {"Last Out": None, "Last Peed": None, "Last Pooped": None}
    with sqlite3.connect("dog_log.db") as conn:
        cursor = conn.cursor()
        for event in summary.keys():
            cursor.execute("SELECT timestamp FROM logs WHERE event=? ORDER BY id DESC LIMIT 1", (event,))
            row = cursor.fetchone()
            if row:
                summary[event] = row[0]
    return jsonify(summary)

@app.route('/get_logs')
def get_logs():
    with sqlite3.connect("dog_log.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, event FROM logs ORDER BY id DESC")
        logs = cursor.fetchall()
    return jsonify(logs)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
