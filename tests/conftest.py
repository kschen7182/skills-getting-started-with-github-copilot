"""Shared fixtures for FastAPI tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset activities to initial state before each test.
    This ensures test isolation and prevents state leakage between tests.
    """
    # Store original activities state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for intramural and varsity competition",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Tennis training and match play for all skill levels",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["jessica@mergington.edu", "ryan@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media art techniques",
            "schedule": "Mondays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["sarah@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting, theater production, and performance workshops",
            "schedule": "Wednesdays and Saturdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["christopher@mergington.edu", "maya@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop critical thinking and public speaking through competitive debate",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["andrew@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore physics, chemistry, biology, and conduct hands-on experiments",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 22,
            "participants": ["rachel@mergington.edu", "tyler@mergington.edu"]
        }
    }
    
    # Clear current activities and restore original state
    activities.clear()
    for name, data in original_activities.items():
        activities[name] = {
            "description": data["description"],
            "schedule": data["schedule"],
            "max_participants": data["max_participants"],
            "participants": data["participants"].copy()  # Create a copy to avoid mutations
        }
    
    yield
    
    # Cleanup after test (optional, but good practice)
    activities.clear()
    for name, data in original_activities.items():
        activities[name] = {
            "description": data["description"],
            "schedule": data["schedule"],
            "max_participants": data["max_participants"],
            "participants": data["participants"].copy()
        }


@pytest.fixture
def client():
    """
    Fixture providing a TestClient for the FastAPI app.
    Activities are reset before each test via the reset_activities fixture.
    """
    return TestClient(app)


@pytest.fixture
def sample_activity_name():
    """Sample activity name that exists in the app."""
    return "Chess Club"


@pytest.fixture
def sample_email():
    """Sample email for a new participant."""
    return "newemail@mergington.edu"


@pytest.fixture
def existing_participant_email():
    """Email of an existing participant in Chess Club."""
    return "michael@mergington.edu"
