"""AI 利用監査ログの生成 (Gemini CLI / Claude Code / Antigravity の3ソース対応)

学術的誠実性(Academic Integrity)の担保のため、AI との対話履歴を日付別の Markdown に
まとめる。詳細な運用ルールは Gemini.md 2章、役割分担は AGENTS.md を参照。

取り込み元:
  1. Gemini CLI   — C:\\Users\\cs16\\.gemini\\tmp\\lab\\chats\\*.jsonl  (自動)
  2. Claude Code  — C:\\Users\\cs16\\.claude\\projects\\c--Users-cs16-lab\\*.jsonl  (自動)
  3. Antigravity  — 進捗報告/antigravity_log/YYYYMMDD.md  (手動記録)

Antigravity だけ手動なのは、ローカルに会話全文が保存されないため。state.vscdb には
base64 protobuf のタイトル要約しか無く、同じ DB に OAuth トークンも入っているので
機械的な解析はしない。Antigravity 自身に記録させる運用にしている(Gemini.md 0章)。

出力: 進捗報告/gemini_log/YYYYMMDD.md
"""

import json
import os
import re
import sqlite3
from datetime import datetime, timedelta, timezone
import glob

# Paths
LOGS_DIR = r'C:\Users\cs16\lab\進捗報告\gemini_log'
DB_PATH = r'C:\Users\cs16\lab\scripts\history.db'
CHATS_PATTERN = r'C:\Users\cs16\.gemini\tmp\lab\chats\*.jsonl'
CLAUDE_PATTERN = r'C:\Users\cs16\.claude\projects\c--Users-cs16-lab\*.jsonl'
ANTIGRAVITY_DIR = r'C:\Users\cs16\lab\進捗報告\antigravity_log'

JST = timezone(timedelta(hours=9))

TOOL_GEMINI = 'Gemini CLI'
TOOL_CLAUDE = 'Claude Code'
TOOL_ANTIGRAVITY = 'Antigravity'

# 表示順
TOOL_ORDER = [TOOL_GEMINI, TOOL_CLAUDE, TOOL_ANTIGRAVITY]


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

    # --- マイグレーション: tool 列の追加 (既存 DB は Gemini CLI 由来として扱う) ---
    for table in ('sessions', 'messages'):
        cols = [r[1] for r in c.execute(f'PRAGMA table_info({table})')]
        if 'tool' not in cols:
            print(f'Migrating: adding "tool" column to {table}')
            c.execute(f"ALTER TABLE {table} ADD COLUMN tool TEXT DEFAULT '{TOOL_GEMINI}'")
            c.execute(f"UPDATE {table} SET tool = ? WHERE tool IS NULL", (TOOL_GEMINI,))

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


def _needs_processing(c, path):
    """未処理 or 更新されたファイルだけ True。"""
    mtime = os.path.getmtime(path)
    c.execute("SELECT mtime FROM processed_files WHERE filename = ?", (os.path.basename(path),))
    row = c.fetchone()
    return (row is None or row[0] < mtime), mtime


# =============================================================================
# 1. Gemini CLI
# =============================================================================

def process_logs(conn):
    files = glob.glob(CHATS_PATTERN)
    c = conn.cursor()

    for f in files:
        todo, mtime = _needs_processing(c, f)
        if not todo:
            continue

        print(f"Processing [Gemini CLI] {os.path.basename(f)}...")
        session_id = None
        with open(f, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    data = json.loads(line)
                    if "sessionId" in data:
                        session_id = data["sessionId"]
                        c.execute("""INSERT OR IGNORE INTO sessions
                                     (session_id, start_time, last_updated, tool)
                                     VALUES (?, ?, ?, ?)""",
                                  (session_id, data["startTime"], data["lastUpdated"], TOOL_GEMINI))
                    elif "id" in data and session_id:
                        msg_id = data["id"]
                        timestamp = data["timestamp"]
                        msg_type = data["type"]
                        content = parse_content(data.get("content", ""))
                        thoughts = json.dumps(data.get("thoughts", []))

                        t_title, t_summary = extract_topic(data)
                        if t_title:
                            c.execute("UPDATE sessions SET title = ? WHERE session_id = ?",
                                      (t_title, session_id))

                        c.execute("""INSERT OR REPLACE INTO messages
                                     (session_id, msg_id, timestamp, type, content, thoughts,
                                      topic_title, topic_summary, tool)
                                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                  (session_id, msg_id, timestamp, msg_type, content, thoughts,
                                   t_title, t_summary, TOOL_GEMINI))
                except Exception as e:
                    print(f"Error parsing line in {f}: {e}")

        c.execute("INSERT OR REPLACE INTO processed_files (filename, mtime) VALUES (?, ?)",
                  (os.path.basename(f), mtime))
    conn.commit()


# =============================================================================
# 2. Claude Code
# =============================================================================

# ツールが自動挿入する制御ブロック。監査ログには不要なので落とす。
_NOISE_RE = re.compile(
    r'<system-reminder>.*?</system-reminder>'
    r'|<ide_opened_file>.*?</ide_opened_file>'
    r'|<ide_selection>.*?</ide_selection>'
    r'|<command-name>.*?</command-name>'
    r'|<command-message>.*?</command-message>'
    r'|<command-args>.*?</command-args>'
    r'|<local-command-stdout>.*?</local-command-stdout>',
    re.S)


def _strip_noise(text):
    return _NOISE_RE.sub('', text or '').strip()


def _to_jst(ts):
    """ISO8601(UTC, 末尾 Z) を JST の 'YYYY-MM-DD HH:MM:SS' にする。"""
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(JST).strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return ts


def _claude_blocks(message):
    """Claude のメッセージから (本文, 思考, 使用ツール名) を取り出す。"""
    content = message.get('content')
    if isinstance(content, str):
        return content, '', []

    texts, thinking, tools = [], [], []
    for b in content or []:
        if not isinstance(b, dict):
            continue
        bt = b.get('type')
        if bt == 'text':
            texts.append(b.get('text', ''))
        elif bt == 'thinking':
            thinking.append(b.get('thinking', ''))
        elif bt == 'tool_use':
            tools.append(b.get('name', '?'))
        # tool_result は出力が長大なので監査ログには含めない
    return "\n".join(texts), "\n".join(thinking), tools


def process_claude_logs(conn):
    files = glob.glob(CLAUDE_PATTERN)
    c = conn.cursor()

    for f in files:
        todo, mtime = _needs_processing(c, f)
        if not todo:
            continue

        print(f"Processing [Claude Code] {os.path.basename(f)}...")
        session_id = os.path.splitext(os.path.basename(f))[0]
        title = None
        first_ts = last_ts = None

        with open(f, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                dtype = data.get('type')
                session_id = data.get('sessionId', session_id)

                if dtype == 'ai-title':
                    title = data.get('aiTitle')
                    continue

                if dtype not in ('user', 'assistant'):
                    continue

                message = data.get('message')
                if not isinstance(message, dict):
                    continue

                ts = _to_jst(data.get('timestamp'))
                if ts:
                    first_ts = ts if first_ts is None else min(first_ts, ts)
                    last_ts = ts if last_ts is None else max(last_ts, ts)

                body, thinking, tools = _claude_blocks(message)
                body = _strip_noise(body)
                if not body:
                    continue  # ツール呼び出しだけの往復は記録しない

                if tools:
                    body += f"\n\n_(使用ツール: {', '.join(sorted(set(tools)))})_"

                c.execute("""INSERT OR REPLACE INTO messages
                             (session_id, msg_id, timestamp, type, content, thoughts,
                              topic_title, topic_summary, tool)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                          (session_id, data.get('uuid'), ts, message.get('role'),
                           body, json.dumps(thinking, ensure_ascii=False),
                           None, None, TOOL_CLAUDE))

        c.execute("""INSERT OR REPLACE INTO sessions
                     (session_id, start_time, last_updated, title, tool)
                     VALUES (?, ?, ?, ?, ?)""",
                  (session_id, first_ts, last_ts, title, TOOL_CLAUDE))
        c.execute("INSERT OR REPLACE INTO processed_files (filename, mtime) VALUES (?, ?)",
                  (os.path.basename(f), mtime))
    conn.commit()


# =============================================================================
# 3. Antigravity (手動記録)
# =============================================================================

def load_antigravity_notes():
    """進捗報告/antigravity_log/YYYYMMDD.md を {'YYYY-MM-DD': 本文} で返す。"""
    notes = {}
    if not os.path.isdir(ANTIGRAVITY_DIR):
        return notes

    for path in sorted(glob.glob(os.path.join(ANTIGRAVITY_DIR, '*.md'))):
        name = os.path.splitext(os.path.basename(path))[0]
        if not re.fullmatch(r'\d{8}', name):
            continue
        d_str = f"{name[:4]}-{name[4:6]}-{name[6:]}"
        with open(path, 'r', encoding='utf-8') as f:
            body = f.read().strip()
        if body:
            notes[d_str] = body
    return notes


# =============================================================================
# レンダリング
# =============================================================================

def render_markdown(conn):
    c = conn.cursor()
    ag_notes = load_antigravity_notes()

    c.execute("SELECT DISTINCT date(timestamp) as msg_date FROM messages WHERE timestamp IS NOT NULL")
    dates = {row[0] for row in c.fetchall() if row[0]}
    dates |= set(ag_notes.keys())

    for d_str in sorted(dates, reverse=True):
        output_file = os.path.join(LOGS_DIR, f"{d_str.replace('-', '')}.md")
        print(f"Rendering {output_file}...")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# AI 利用監査ログ：{d_str}\n\n")
            f.write("> このログは `scripts/render_llm_history.py` が自動生成しています。手で編集しないでください。\n")
            f.write("> 取り込み元: Gemini CLI / Claude Code (自動)、Antigravity (手動記録)\n\n")

            for tool in TOOL_ORDER:
                if tool == TOOL_ANTIGRAVITY:
                    if d_str in ag_notes:
                        f.write(f"# {tool}\n\n")
                        f.write(ag_notes[d_str] + "\n\n---\n\n")
                    continue

                c.execute("""SELECT DISTINCT s.session_id, s.title, s.start_time
                             FROM sessions s
                             JOIN messages m ON s.session_id = m.session_id
                             WHERE date(m.timestamp) = ? AND m.tool = ?
                             ORDER BY s.start_time ASC""", (d_str, tool))
                sessions = c.fetchall()
                if not sessions:
                    continue

                f.write(f"# {tool}\n\n")

                for s_id, s_title, s_start in sessions:
                    title = s_title if s_title else f"Session {s_id[:8]}"
                    f.write(f"## {title}\n")
                    f.write(f"- **Session ID**: `{s_id}`\n")
                    f.write(f"- **開始時刻**: `{s_start}`\n\n")

                    c.execute("""SELECT type, content, timestamp, topic_title, topic_summary
                                 FROM messages
                                 WHERE session_id = ? AND date(timestamp) = ? AND tool = ?
                                 ORDER BY timestamp ASC""", (s_id, d_str, tool))

                    for m_type, m_content, m_time, mt_title, mt_summary in c.fetchall():
                        if mt_title:
                            f.write(f"### Topic Update: {mt_title}\n")
                            if mt_summary:
                                f.write(f"{mt_summary}\n\n")

                        if not (m_content or '').strip():
                            continue

                        role = "User" if m_type == "user" else tool
                        f.write(f"**[{m_time}] {role}**:\n")
                        indented = "\n".join(f"> {line}" for line in m_content.strip().split("\n"))
                        f.write(f"{indented}\n\n")

                    f.write("---\n\n")


if __name__ == '__main__':
    for d in (LOGS_DIR, ANTIGRAVITY_DIR):
        if not os.path.exists(d):
            os.makedirs(d)
    conn = setup_db()
    process_logs(conn)
    process_claude_logs(conn)
    render_markdown(conn)
    conn.close()
    print("Done.")
