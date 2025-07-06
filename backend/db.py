
import sqlite3

def init_db():
    conn = sqlite3.connect("agent.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS agent_actions (
        timestamp TEXT,
        agent_name TEXT,
        action_type TEXT,
        details TEXT
    )''')
    conn.commit()
    conn.close()

def save_action(timestamp, agent_name, action_type, details):
    conn = sqlite3.connect("agent.db")
    c = conn.cursor()
    c.execute("INSERT INTO agent_actions VALUES (?, ?, ?, ?)",
              (timestamp, agent_name, action_type, details))
    conn.commit()
    conn.close()

def get_all_actions():
    conn = sqlite3.connect("agent.db")
    c = conn.cursor()
    c.execute("SELECT * FROM agent_actions ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return [
        {"timestamp": r[0], "agent_name": r[1], "action_type": r[2], "details": r[3]}
        for r in rows
    ]
