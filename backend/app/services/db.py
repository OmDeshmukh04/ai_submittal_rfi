import sqlite3, os, json
BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data")
os.makedirs(os.path.join(BASE, "submittals"), exist_ok=True)
DB_PATH = os.path.join(BASE, "app.db")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS submittals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    text TEXT,
    status TEXT,
    quick_flags TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def save_submittal(filename: str, text: str, status: str = "uploaded", quick_flags=None) -> int:
    qf = json.dumps(quick_flags or [])
    c.execute("INSERT INTO submittals (filename, text, status, quick_flags) VALUES (?, ?, ?, ?)",
              (filename, text, status, qf))
    conn.commit()
    return c.lastrowid

def update_submittal_text(sub_id: int, new_text: str):
    c.execute("UPDATE submittals SET text=?, status=?, quick_flags=? WHERE id=?",
              (new_text, "ocr_done", json.dumps([]), sub_id))
    conn.commit()

def get_submittal(sub_id: int):
    r = c.execute("SELECT id, filename, status, quick_flags FROM submittals WHERE id=?", (sub_id,)).fetchone()
    return r
