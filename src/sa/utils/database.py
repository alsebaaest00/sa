"""Database management for SA Platform"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

# Database path
DB_PATH = Path("data/sa.db")
DB_PATH.parent.mkdir(exist_ok=True)


class Database:
    """SQLite database manager for projects and statistics"""

    def __init__(self, db_path: str = str(DB_PATH)):
        """Initialize database"""
        self.db_path = db_path
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Projects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                images TEXT,
                videos TEXT,
                audio TEXT
            )
        """)

        # Generations table (لتتبع العمليات)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS generations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                type TEXT,
                prompt TEXT,
                file_path TEXT,
                duration REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        """)

        # Statistics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                images_count INTEGER DEFAULT 0,
                videos_count INTEGER DEFAULT 0,
                audio_count INTEGER DEFAULT 0,
                total_time REAL DEFAULT 0,
                UNIQUE(date)
            )
        """)

        conn.commit()
        conn.close()

    def create_project(self, name: str, description: str = "") -> int:
        """Create a new project"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO projects (name, description) VALUES (?, ?)",
            (name, description),
        )

        project_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return int(project_id) if project_id else 0

    def get_projects(self) -> list[dict[str, Any]]:
        """Get all projects"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
        projects = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return projects

    def get_project(self, project_id: int) -> dict[str, Any] | None:
        """Get specific project"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()

        conn.close()
        return dict(row) if row else None

    def update_project(
        self, project_id: int, name: str | None = None, description: str | None = None
    ) -> None:
        """Update project"""
        conn = self.get_connection()
        cursor = conn.cursor()

        if name and description:
            cursor.execute(
                "UPDATE projects SET name = ?, description = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (name, description, project_id),
            )
        elif name:
            cursor.execute(
                "UPDATE projects SET name = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (name, project_id),
            )
        elif description:
            cursor.execute(
                "UPDATE projects SET description = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (description, project_id),
            )

        conn.commit()
        conn.close()

    def delete_project(self, project_id: int) -> None:
        """Delete project"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM generations WHERE project_id = ?", (project_id,))
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))

        conn.commit()
        conn.close()

    def add_generation(
        self,
        project_id: int,
        gen_type: str,
        prompt: str,
        file_path: str,
        duration: float = 0,
    ) -> None:
        """Add a generation record"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO generations (project_id, type, prompt, file_path, duration)
               VALUES (?, ?, ?, ?, ?)""",
            (project_id, gen_type, prompt, file_path, duration),
        )

        conn.commit()
        conn.close()

        # Update statistics
        self._update_stats(gen_type, duration)

    def get_generations(self, project_id: int) -> list[dict[str, Any]]:
        """Get project generations"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT * FROM generations WHERE project_id = ?
               ORDER BY created_at DESC""",
            (project_id,),
        )
        generations = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return generations

    def get_statistics(self, date: str | None = None) -> dict[str, Any]:
        """Get statistics"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM statistics WHERE date = ?", (date,))
        row = cursor.fetchone()

        conn.close()

        if row:
            return dict(row)

        return {
            "date": date,
            "images_count": 0,
            "videos_count": 0,
            "audio_count": 0,
            "total_time": 0,
        }

    def get_all_statistics(self) -> list[dict[str, Any]]:
        """Get all statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM statistics ORDER BY date DESC")
        stats = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return stats

    def _update_stats(self, gen_type: str, duration: float) -> None:
        """Update daily statistics"""
        date = datetime.now().strftime("%Y-%m-%d")
        conn = self.get_connection()
        cursor = conn.cursor()

        # Check if record exists
        cursor.execute("SELECT id FROM statistics WHERE date = ?", (date,))
        exists = cursor.fetchone()

        if exists:
            if gen_type == "image":
                cursor.execute(
                    "UPDATE statistics SET images_count = images_count + 1, total_time = total_time + ? WHERE date = ?",
                    (duration, date),
                )
            elif gen_type == "video":
                cursor.execute(
                    "UPDATE statistics SET videos_count = videos_count + 1, total_time = total_time + ? WHERE date = ?",
                    (duration, date),
                )
            elif gen_type == "audio":
                cursor.execute(
                    "UPDATE statistics SET audio_count = audio_count + 1, total_time = total_time + ? WHERE date = ?",
                    (duration, date),
                )
        else:
            if gen_type == "image":
                cursor.execute(
                    "INSERT INTO statistics (date, images_count, total_time) VALUES (?, 1, ?)",
                    (date, duration),
                )
            elif gen_type == "video":
                cursor.execute(
                    "INSERT INTO statistics (date, videos_count, total_time) VALUES (?, 1, ?)",
                    (date, duration),
                )
            elif gen_type == "audio":
                cursor.execute(
                    "INSERT INTO statistics (date, audio_count, total_time) VALUES (?, 1, ?)",
                    (date, duration),
                )

        conn.commit()
        conn.close()

    def export_project(self, project_id: int) -> str:
        """Export project as JSON"""
        project = self.get_project(project_id)
        generations = self.get_generations(project_id)

        export_data = {"project": project, "generations": generations}

        return json.dumps(export_data, indent=2, default=str)


# Global database instance
db = Database()
