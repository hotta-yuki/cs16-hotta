
import json
import os
import sqlite3
from datetime import datetime
import glob
import re

# Paths
LOGS_DIR = r'C:\Users\cs16\lab\進捗報告\gemini_log'
DB_PATH = r'C:\Users\cs16\lab\scripts\history.db'
CHATS_PATTERN = r'C:\Users\cs16\.gemini\tmp\lab\chats\*.jsonl'

def setup_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS processed_files (
                    filename TEXT PRIMARY KEY,
                    mtime REAL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
                    session_id TEXT,
                    msg_id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    type TEXT,
                    content TEXT,
                    thoughts TEXT,
                    topic_title TEXT,
                    topic_summary TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    start_time TEXT,
                    last_updated TEXT,
                    title TEXT
                )''')
    conn.commit()
    return conn

def parse_content(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join([c.get("text", "") for c in content if isinstance(c, dict)])
    return str(content)

def extract_topic(data):
    """Extract topic info from toolCalls if present."""
    if "toolCalls" in data:
        for tc in data["toolCalls"]:
            if tc.get("name") == "update_topic":
                args = tc.get("args", {})
                return args.get("title"), args.get("summary")
    return None, None

def process_logs(conn):
    files = glob.glob(CHATS_PATTERN)
    c = conn.cursor()
    
    for f in files:
        mtime = os.path.getmtime(f)
        c.execute("SELECT mtime FROM processed_files WHERE filename = ?", (os.path.basename(f),))
        row = c.fetchone()
        if row and row[0] >= mtime:
            continue
        
        print(f"Processing {os.path.basename(f)}...")
        session_id = None
        with open(f, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    data = json.loads(line)
                    if "sessionId" in data:
                        session_id = data["sessionId"]
                        c.execute("INSERT OR IGNORE INTO sessions (session_id, start_time, last_updated) VALUES (?, ?, ?)",
                                  (session_id, data["startTime"], data["lastUpdated"]))
                    elif "id" in data and session_id:
                        msg_id = data["id"]
                        timestamp = data["timestamp"]
                        msg_type = data["type"]
                        content = parse_content(data.get("content", ""))
                        thoughts_data = data.get("thoughts", [])
                        thoughts = json.dumps(thoughts_data)
                        
                        t_title, t_summary = extract_topic(data)
                        if t_title:
                            c.execute("UPDATE sessions SET title = ? WHERE session_id = ?", (t_title, session_id))

                        c.execute("""INSERT OR REPLACE INTO messages 
                                     (session_id, msg_id, timestamp, type, content, thoughts, topic_title, topic_summary) 
                                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                  (session_id, msg_id, timestamp, msg_type, content, thoughts, t_title, t_summary))
                except Exception as e:
                    print(f"Error parsing line in {f}: {e}")
        
        c.execute("INSERT OR REPLACE INTO processed_files (filename, mtime) VALUES (?, ?)", (os.path.basename(f), mtime))
    conn.commit()

def render_markdown(conn):
    c = conn.cursor()
    c.execute("SELECT DISTINCT date(timestamp) as msg_date FROM messages ORDER BY msg_date DESC")
    dates = [row[0] for row in c.fetchall()]
    
    for d_str in dates:
        output_file = os.path.join(LOGS_DIR, f"{d_str.replace('-', '')}.md")
        print(f"Rendering {output_file}...")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# AI 利用監査ログ：{d_str}\n\n")
            f.write("> このログは自動生成システムによって管理されています。\n\n")
            
            c.execute("""SELECT DISTINCT s.session_id, s.title, s.start_time 
                         FROM sessions s 
                         JOIN messages m ON s.session_id = m.session_id 
                         WHERE date(m.timestamp) = ? 
                         ORDER BY s.start_time ASC""", (d_str,))
            sessions = c.fetchall()
            
            for s_id, s_title, s_start in sessions:
                # Use current title from DB
                title = s_title if s_title else f"Session {s_id[:8]}"
                f.write(f"## {title}\n")
                f.write(f"- **Session ID**: `{s_id}`\n")
                f.write(f"- **開始時刻**: `{s_start}`\n\n")
                
                c.execute("""SELECT type, content, timestamp, topic_title, topic_summary 
                             FROM messages 
                             WHERE session_id = ? AND date(timestamp) = ? 
                             ORDER BY timestamp ASC""", (s_id, d_str))
                msgs = c.fetchall()
                
                for m_type, m_content, m_time, mt_title, mt_summary in msgs:
                    if mt_title:
                        f.write(f"### 唐 Topic Update: {mt_title}\n")
                        if mt_summary:
                            f.write(f"{mt_summary}\n\n")
                    
                    if not m_content.strip(): continue
                    
                    role = "User" if m_type == "user" else "Gemini"
                    f.write(f"**[{m_time}] {role}**:\n")
                    content_indented = "\n".join([f"> {line}" for line in m_content.strip().split("\n")])
                    f.write(f"{content_indented}\n\n")
                
                f.write("---\n\n")

if __name__ == '__main__':
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
    conn = setup_db()
    process_logs(conn)
    render_markdown(conn)
    conn.close()
