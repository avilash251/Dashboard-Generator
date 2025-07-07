def get_prompt_trend():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT DATE(timestamp) as date, COUNT(*) as count
            FROM prompt_logs
            GROUP BY DATE(timestamp)
            ORDER BY DATE(timestamp)
        """)
        return [{"date": row[0], "count": row[1]} for row in c.fetchall()]
