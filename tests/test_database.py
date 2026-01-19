"""Tests for database module"""

import os
import tempfile

import pytest
from sa.utils.database import Database


@pytest.fixture
def temp_db():
    """Create temporary database for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db = Database(db_path)
        yield db
        # Cleanup
        if os.path.exists(db_path):
            os.remove(db_path)


def test_create_project(temp_db):
    """Test project creation"""
    project_id = temp_db.create_project("Test Project", "Test Description")
    assert project_id > 0


def test_get_project(temp_db):
    """Test getting project"""
    project_id = temp_db.create_project("Test", "Desc")
    project = temp_db.get_project(project_id)
    assert project is not None
    assert project["name"] == "Test"
    assert project["description"] == "Desc"


def test_list_projects(temp_db):
    """Test listing projects"""
    temp_db.create_project("Project 1", "Desc 1")
    temp_db.create_project("Project 2", "Desc 2")
    projects = temp_db.get_projects()
    assert len(projects) == 2


def test_update_project(temp_db):
    """Test updating project"""
    project_id = temp_db.create_project("Old Name", "Old Desc")
    temp_db.update_project(project_id, "New Name", "New Desc")
    project = temp_db.get_project(project_id)
    assert project["name"] == "New Name"
    assert project["description"] == "New Desc"


def test_delete_project(temp_db):
    """Test deleting project"""
    project_id = temp_db.create_project("To Delete", "Desc")
    temp_db.delete_project(project_id)
    project = temp_db.get_project(project_id)
    assert project is None


def test_add_generation(temp_db):
    """Test adding generation"""
    project_id = temp_db.create_project("Test", "Desc")
    temp_db.add_generation(project_id, "image", "test prompt", "/path/to/image.png", 5.0)
    generations = temp_db.get_generations(project_id)
    assert len(generations) == 1
    assert generations[0]["type"] == "image"


def test_statistics(temp_db):
    """Test statistics tracking"""
    project_id = temp_db.create_project("Test", "Desc")

    # Add some generations
    temp_db.add_generation(project_id, "image", "prompt1", "/path/1.png", 2.0)
    temp_db.add_generation(project_id, "image", "prompt2", "/path/2.png", 3.0)
    temp_db.add_generation(project_id, "video", "prompt3", "/path/3.mp4", 10.0)

    # Get statistics
    stats = temp_db.get_statistics()
    assert stats["images_count"] == 2
    assert stats["videos_count"] == 1
    assert stats["total_time"] == 15.0


def test_get_nonexistent_project(temp_db):
    """Test getting non-existent project"""
    project = temp_db.get_project(9999)
    assert project is None


def test_update_project_name_only(temp_db):
    """Test updating only project name"""
    project_id = temp_db.create_project("Old", "Desc")
    temp_db.update_project(project_id, name="New")
    project = temp_db.get_project(project_id)
    assert project["name"] == "New"


def test_update_project_description_only(temp_db):
    """Test updating only description"""
    project_id = temp_db.create_project("Name", "Old Desc")
    temp_db.update_project(project_id, description="New Desc")
    project = temp_db.get_project(project_id)
    assert project["description"] == "New Desc"


def test_multiple_generations(temp_db):
    """Test multiple generations for one project"""
    project_id = temp_db.create_project("Multi", "Test")

    for i in range(5):
        temp_db.add_generation(project_id, "image", f"prompt{i}", f"/path/{i}.png", 1.0)

    generations = temp_db.get_generations(project_id)
    assert len(generations) == 5


def test_empty_generations(temp_db):
    """Test getting generations for project with none"""
    project_id = temp_db.create_project("Empty", "No gens")
    generations = temp_db.get_generations(project_id)
    assert len(generations) == 0


def test_statistics_no_data(temp_db):
    """Test statistics with no data"""
    stats = temp_db.get_statistics()
    assert stats["images_count"] == 0
    assert stats["videos_count"] == 0
