import sqlite3
import os
import shutil
from datetime import datetime
from utils.logger import log_info, log_error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "history.db")
DB_BACKUP_PATH = os.path.join(BASE_DIR, "db", "history_backup.db")


def backup_database():
    """Create a backup of the database."""
    try:
        if os.path.exists(DB_PATH):
            shutil.copy2(DB_PATH, DB_BACKUP_PATH)
            log_info(f"Database backed up to {DB_BACKUP_PATH}")
            return True
    except Exception as e:
        log_error(f"Failed to backup database: {e}")
    return False


def restore_from_backup():
    """Restore database from backup."""
    try:
        if os.path.exists(DB_BACKUP_PATH):
            shutil.copy2(DB_BACKUP_PATH, DB_PATH)
            log_info("Database restored from backup")
            return True
    except Exception as e:
        log_error(f"Failed to restore from backup: {e}")
    return False


def verify_database_integrity() -> bool:
    """Check if database is not corrupted."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        conn.close()
        
        is_ok = result[0] == "ok"
        if is_ok:
            log_info("Database integrity check passed")
        else:
            log_error(f"Database integrity check failed: {result[0]}")
        return is_ok
    except Exception as e:
        log_error(f"Database integrity check error: {e}")
        return False


def init_db():
    """Initialize database with corruption handling."""
    try:
        # Check if database exists and is corrupted
        if os.path.exists(DB_PATH):
            if not verify_database_integrity():
                log_error("Database is corrupted. Attempting recovery...")
                
                # Try to restore from backup
                if restore_from_backup():
                    if verify_database_integrity():
                        log_info("Successfully restored from backup")
                        return
                
                # If backup fails, create new database
                log_error("Backup restoration failed. Creating new database...")
                os.remove(DB_PATH)
        
        # Create/recreate database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        
        log_info("Database initialized successfully")
        
        # Create initial backup
        backup_database()
        
    except Exception as e:
        log_error(f"Critical error initializing database: {e}")
        raise


def save_history(query: str, response: str):
    """Save query history with error handling and backup."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        c = conn.cursor()
        c.execute(
            "INSERT INTO history (query, response, timestamp) VALUES (?, ?, ?)",
            (query, response, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
        
        # Periodic backup (every 10 entries)
        if get_entry_count() % 10 == 0:
            backup_database()
            
    except sqlite3.OperationalError as e:
        log_error(f"Database operation failed: {e}")
        
        # Try to recover
        if not verify_database_integrity():
            restore_from_backup()
            
        # Retry once
        try:
            conn = sqlite3.connect(DB_PATH, timeout=10.0)
            c = conn.cursor()
            c.execute(
                "INSERT INTO history (query, response, timestamp) VALUES (?, ?, ?)",
                (query, response, datetime.now().isoformat())
            )
            conn.commit()
            conn.close()
        except Exception as retry_error:
            log_error(f"Retry failed: {retry_error}")
            
    except Exception as e:
        log_error(f"Unexpected error saving history: {e}")


def get_history():
    """Get query history with error handling."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        c = conn.cursor()
        c.execute("SELECT id, query, response, timestamp FROM history ORDER BY id DESC LIMIT 10")
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception as e:
        log_error(f"Error retrieving history: {e}")
        return []


def get_entry_count() -> int:
    """Get total number of entries in database."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM history")
        count = c.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        log_error(f"Error getting entry count: {e}")
        return 0


# Initialize DB on import
init_db()