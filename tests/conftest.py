"""Shared pytest fixtures for the Mergington High School API tests."""

import copy

import pytest
from fastapi.testclient import TestClient

from app import activities, app


@pytest.fixture
def client():
    """Provide a FastAPI TestClient bound to the app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Snapshot the in-memory activities dict and restore it after each test.

    This keeps state isolated between tests so signup/unregister tests do not
    pollute each other.
    """
    snapshot = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(snapshot)
