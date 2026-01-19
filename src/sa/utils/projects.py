"""Project management for SA Platform"""

from typing import Any

from .database import db


class ProjectManager:
    """Manage projects and their content"""

    @staticmethod
    def create_project(name: str, description: str = "") -> int:
        """Create new project"""
        return db.create_project(name, description)

    @staticmethod
    def list_projects() -> list[dict[str, Any]]:
        """List all projects"""
        return db.get_projects()

    @staticmethod
    def get_project(project_id: int) -> dict[str, Any] | None:
        """Get project details"""
        return db.get_project(project_id)

    @staticmethod
    def update_project(
        project_id: int, name: str | None = None, description: str | None = None
    ) -> None:
        """Update project"""
        db.update_project(project_id, name, description)

    @staticmethod
    def delete_project(project_id: int) -> None:
        """Delete project"""
        db.delete_project(project_id)

    @staticmethod
    def add_generation(
        project_id: int,
        gen_type: str,
        prompt: str,
        file_path: str,
        duration: float = 0,
    ) -> None:
        """Add generation to project"""
        db.add_generation(project_id, gen_type, prompt, file_path, duration)

    @staticmethod
    def get_generations(project_id: int) -> list[dict[str, Any]]:
        """Get project generations"""
        return db.get_generations(project_id)

    @staticmethod
    def get_statistics(date: str | None = None) -> dict[str, Any]:
        """Get daily statistics"""
        return db.get_statistics(date)

    @staticmethod
    def get_all_statistics() -> list[dict[str, Any]]:
        """Get all statistics"""
        return db.get_all_statistics()

    @staticmethod
    def export_project(project_id: int) -> str:
        """Export project as JSON"""
        return db.export_project(project_id)


# Global project manager instance
project_manager = ProjectManager()
