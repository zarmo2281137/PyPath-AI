from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import sqlite3
import subprocess
import sys
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from fastapi import Cookie, Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from curriculum import CURRICULUM
from curriculum_details import TOPIC_DETAILS

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "learning.db"
STATIC_DIR = BASE_DIR / "static"

SESSION_COOKIE_NAME = "pypath_session"
SESSION_TTL_DAYS = 30

VALID_TOPIC_IDS: set[str] = {
    topic["id"] for stage in CURRICULUM for topic in stage["topics"]
}

app = FastAPI(title="PyPath AI — Навчальна платформа", version="2.0.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def today_iso() -> str:
    return date.today().isoformat()


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_db() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                display_name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS topic_progress (
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                topic_id TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                notes TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL,
                PRIMARY KEY (user_id, topic_id)
            );

            CREATE TABLE IF NOT EXISTS quiz_results (
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                topic_id TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (user_id, topic_id)
            );

            CREATE TABLE IF NOT EXISTS study_activity (
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                activity_date TEXT NOT NULL,
                xp INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (user_id, activity_date)
            );
            """
        )


init_db()


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 200_000
    ).hex()
    return f"{salt}${digest}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt, expected_digest = stored_hash.split("$", 1)
    except ValueError:
        return False
    actual_digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 200_000
    ).hex()
    return hmac.compare_digest(actual_digest, expected_digest)


def create_session(conn: sqlite3.Connection, user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    now = datetime.now(timezone.utc)
    expires = now + timedelta(days=SESSION_TTL_DAYS)
    conn.execute(
        "INSERT INTO sessions (token, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)",
        (token, user_id, now.isoformat(), expires.isoformat()),
    )
    return token


def set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        max_age=SESSION_TTL_DAYS * 24 * 60 * 60,
        path="/",
    )


def add_xp(conn: sqlite3.Connection, user_id: int, xp_delta: int) -> None:
    if xp_delta <= 0:
        return
    conn.execute(
        """
        INSERT INTO study_activity (user_id, activity_date, xp)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, activity_date) DO UPDATE SET
            xp = study_activity.xp + excluded.xp
        """,
        (user_id, today_iso(), xp_delta),
    )


def compute_streak(conn: sqlite3.Connection, user_id: int) -> tuple[int, int]:
    rows = conn.execute(
        "SELECT activity_date, xp FROM study_activity WHERE user_id = ? ORDER BY activity_date DESC",
        (user_id,),
    ).fetchall()
    total_xp = sum(r["xp"] for r in rows)
    active_dates = {date.fromisoformat(r["activity_date"]) for r in rows if r["xp"] > 0}
    if not active_dates:
        return 0, total_xp

    today = date.today()
    cursor = today if today in active_dates else today - timedelta(days=1)
    streak = 0
    while cursor in active_dates:
        streak += 1
        cursor -= timedelta(days=1)
    return streak, total_xp


def get_optional_user(
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
) -> dict[str, Any] | None:
    if not session_token:
        return None
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT u.id, u.username, u.display_name, u.created_at, s.expires_at
            FROM sessions s
            JOIN users u ON u.id = s.user_id
            WHERE s.token = ?
            """,
            (session_token,),
        ).fetchone()
        if not row:
            return None
        if datetime.fromisoformat(row["expires_at"]) < datetime.now(timezone.utc):
            conn.execute("DELETE FROM sessions WHERE token = ?", (session_token,))
            return None
        return {
            "id": row["id"],
            "username": row["username"],
            "display_name": row["display_name"],
            "created_at": row["created_at"],
        }


def require_user(
    user: dict[str, Any] | None = Depends(get_optional_user),
) -> dict[str, Any]:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Потрібно увійти в акаунт для збереження прогресу.",
        )
    return user


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    display_name: str = Field(default="", max_length=50)
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=32)
    password: str = Field(min_length=1, max_length=128)


class TopicProgressUpdate(BaseModel):
    completed: bool | None = None
    notes: str | None = Field(default=None, max_length=4000)


class BulkProgressSync(BaseModel):
    completed_ids: list[str] = Field(default_factory=list)


class QuizSubmission(BaseModel):
    answers: list[int] = Field(default_factory=list)


class PlaygroundRequest(BaseModel):
    code: str = Field(min_length=1, max_length=4000)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/curriculum")
def get_curriculum() -> dict[str, Any]:
    enriched_stages = []
    for stage in CURRICULUM:
        topics = []
        for topic in stage["topics"]:
            details = TOPIC_DETAILS.get(topic["id"], {})
            quiz_public = [
                {"q": item["q"], "options": item["options"]}
                for item in details.get("quiz", [])
            ]
            topics.append(
                {
                    **topic,
                    "theory": details.get("theory", []),
                    "code": details.get("code", ""),
                    "docs": details.get("docs", []),
                    "interview": details.get("interview"),
                    "quiz": quiz_public,
                }
            )
        enriched_stages.append({**stage, "topics": topics})
    return {"stages": enriched_stages}


@app.get("/api/auth/me")
def auth_me(user: dict[str, Any] | None = Depends(get_optional_user)) -> dict[str, Any]:
    return {"user": user}


@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, response: Response) -> dict[str, Any]:
    username = payload.username.strip().lower()
    if not username.replace("_", "").replace("-", "").isalnum():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Логін може містити лише латинські літери, цифри, '_' або '-'.",
        )
    display_name = payload.display_name.strip() or payload.username.strip()
    pw_hash = hash_password(payload.password)

    with get_db() as conn:
        existing = conn.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Користувач із таким логіном вже існує.",
            )
        cursor = conn.execute(
            "INSERT INTO users (username, display_name, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (username, display_name, pw_hash, utc_now_iso()),
        )
        user_id = cursor.lastrowid
        assert user_id is not None
        token = create_session(conn, user_id)
        set_session_cookie(response, token)
        user_row = conn.execute(
            "SELECT id, username, display_name, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()

    return {"user": dict(user_row)}


@app.post("/api/auth/login")
def login(payload: LoginRequest, response: Response) -> dict[str, Any]:
    username = payload.username.strip().lower()
    with get_db() as conn:
        user_row = conn.execute(
            "SELECT id, username, display_name, password_hash, created_at FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        if not user_row or not verify_password(payload.password, user_row["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невірний логін або пароль.",
            )
        token = create_session(conn, user_row["id"])
        set_session_cookie(response, token)

    return {
        "user": {
            "id": user_row["id"],
            "username": user_row["username"],
            "display_name": user_row["display_name"],
            "created_at": user_row["created_at"],
        }
    }


@app.post("/api/auth/logout")
def logout(
    response: Response,
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
) -> dict[str, bool]:
    if session_token:
        with get_db() as conn:
            conn.execute("DELETE FROM sessions WHERE token = ?", (session_token,))
    response.delete_cookie(key=SESSION_COOKIE_NAME, path="/")
    return {"ok": True}


@app.get("/api/progress")
def get_progress(user: dict[str, Any] = Depends(require_user)) -> dict[str, Any]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT topic_id, completed, notes FROM topic_progress WHERE user_id = ?",
            (user["id"],),
        ).fetchall()
        quiz_rows = conn.execute(
            "SELECT topic_id, score, total FROM quiz_results WHERE user_id = ?",
            (user["id"],),
        ).fetchall()
        streak_days, total_xp = compute_streak(conn, user["id"])

    completed = [r["topic_id"] for r in rows if r["completed"]]
    notes = {r["topic_id"]: r["notes"] for r in rows if r["notes"]}
    quiz_results = {
        r["topic_id"]: {"score": r["score"], "total": r["total"]} for r in quiz_rows
    }
    return {
        "completed": completed,
        "notes": notes,
        "quiz_results": quiz_results,
        "streak_days": streak_days,
        "total_xp": total_xp,
    }


@app.put("/api/progress/{topic_id}")
def update_topic_progress(
    topic_id: str,
    payload: TopicProgressUpdate,
    user: dict[str, Any] = Depends(require_user),
) -> dict[str, Any]:
    if topic_id not in VALID_TOPIC_IDS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тему не знайдено в програмі.",
        )

    now = utc_now_iso()
    with get_db() as conn:
        existing = conn.execute(
            "SELECT completed, notes FROM topic_progress WHERE user_id = ? AND topic_id = ?",
            (user["id"], topic_id),
        ).fetchone()

        was_completed = bool(existing["completed"]) if existing else False
        new_completed = (
            int(payload.completed)
            if payload.completed is not None
            else (existing["completed"] if existing else 0)
        )
        new_notes = (
            payload.notes
            if payload.notes is not None
            else (existing["notes"] if existing else "")
        )

        conn.execute(
            """
            INSERT INTO topic_progress (user_id, topic_id, completed, notes, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, topic_id) DO UPDATE SET
                completed = excluded.completed,
                notes = excluded.notes,
                updated_at = excluded.updated_at
            """,
            (user["id"], topic_id, new_completed, new_notes, now),
        )

        if not was_completed and new_completed:
            add_xp(conn, user["id"], 20)
        elif payload.notes is not None and payload.notes.strip():
            add_xp(conn, user["id"], 5)

        streak_days, total_xp = compute_streak(conn, user["id"])

    return {
        "topic_id": topic_id,
        "completed": bool(new_completed),
        "notes": new_notes,
        "updated_at": now,
        "streak_days": streak_days,
        "total_xp": total_xp,
    }


@app.post("/api/progress/bulk")
def sync_bulk_progress(
    payload: BulkProgressSync,
    user: dict[str, Any] = Depends(require_user),
) -> dict[str, Any]:
    now = utc_now_iso()
    valid_ids = [tid for tid in payload.completed_ids if tid in VALID_TOPIC_IDS]
    with get_db() as conn:
        for tid in valid_ids:
            conn.execute(
                """
                INSERT INTO topic_progress (user_id, topic_id, completed, notes, updated_at)
                VALUES (?, ?, 1, '', ?)
                ON CONFLICT(user_id, topic_id) DO UPDATE SET
                    completed = 1,
                    updated_at = excluded.updated_at
                """,
                (user["id"], tid, now),
            )
        if valid_ids:
            add_xp(conn, user["id"], 20 * len(valid_ids))
    return {"synced_count": len(valid_ids)}


@app.post("/api/quiz/{topic_id}")
def submit_quiz(
    topic_id: str,
    payload: QuizSubmission,
    user: dict[str, Any] | None = Depends(get_optional_user),
) -> dict[str, Any]:
    details = TOPIC_DETAILS.get(topic_id)
    if not details or not details.get("quiz"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тест для цієї теми не знайдено.",
        )

    quiz_items = details["quiz"]
    total = len(quiz_items)
    if len(payload.answers) != total:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Потрібно відповісти на всі питання тесту.",
        )

    correct_indices = [item["answer"] for item in quiz_items]
    score = sum(1 for a, c in zip(payload.answers, correct_indices) if a == c)
    passed = score == total
    xp_earned = 0

    streak_days = 0
    total_xp = 0
    if user:
        with get_db() as conn:
            prev = conn.execute(
                "SELECT score, total FROM quiz_results WHERE user_id = ? AND topic_id = ?",
                (user["id"], topic_id),
            ).fetchone()
            best_score = max(score, prev["score"]) if prev else score
            conn.execute(
                """
                INSERT INTO quiz_results (user_id, topic_id, score, total, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id, topic_id) DO UPDATE SET
                    score = excluded.score,
                    total = excluded.total,
                    updated_at = excluded.updated_at
                """,
                (user["id"], topic_id, best_score, total, utc_now_iso()),
            )
            if passed and (not prev or prev["score"] < total):
                xp_earned = 30
                add_xp(conn, user["id"], xp_earned)
            streak_days, total_xp = compute_streak(conn, user["id"])

    return {
        "topic_id": topic_id,
        "score": score,
        "total": total,
        "passed": passed,
        "correct_indices": correct_indices,
        "xp_earned": xp_earned,
        "saved": bool(user),
        "streak_days": streak_days,
        "total_xp": total_xp,
    }


@app.post("/api/playground/run")
def run_python_playground(payload: PlaygroundRequest) -> dict[str, Any]:
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    try:
        proc = subprocess.run(
            [sys.executable, "-X", "utf8", "-I", "-c", payload.code],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=3,
            env=env,
        )
        return {
            "stdout": proc.stdout[:8000],
            "stderr": proc.stderr[:4000],
            "returncode": proc.returncode,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Час виконання перевищено (ліміт 3 секунди). Перевірте, чи немає нескінченного циклу.",
            "returncode": -1,
            "timed_out": True,
        }
