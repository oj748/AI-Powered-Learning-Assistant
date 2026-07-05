import sqlite3
from config import PROJECT_ROOT
DB_PATH = PROJECT_ROOT / "learning_assistant.db"


def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


def setup_database():

    conn = get_connection()

    cursor = conn.cursor()

    # ==========================
    # Notes
    # ==========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
        
            title TEXT NOT NULL UNIQUE,
        
            content TEXT NOT NULL DEFAULT '',
        
            created_at TIMESTAMP
                DEFAULT (datetime('now','localtime')),
        
            updated_at TIMESTAMP
                DEFAULT (datetime('now','localtime'))
        )
    """)

    # ==========================
    # Decks
    # ==========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
        
            name TEXT NOT NULL UNIQUE,
        
            created_at TIMESTAMP
                DEFAULT (datetime('now','localtime'))
        )
    """)

    # ==========================
    # Flashcards
    # ==========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
        
            deck_id INTEGER NOT NULL,
        
            front TEXT NOT NULL,
        
            back TEXT NOT NULL,
        
            interval_days INTEGER
                DEFAULT 1,
        
            ease_factor REAL
                DEFAULT 2.5,
        
            review_count INTEGER
                DEFAULT 0,
        
            last_review TIMESTAMP,
        
            next_review TIMESTAMP
                DEFAULT (datetime('now','localtime')),
        
            created_at TIMESTAMP
                DEFAULT (datetime('now','localtime')),
        
            FOREIGN KEY(deck_id)
                REFERENCES decks(id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()

    conn.close()