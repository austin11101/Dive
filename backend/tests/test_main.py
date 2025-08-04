import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    """Test the main endpoint"""
    response = client.get("/")
    assert response.status_code == 200

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_docs_endpoint():
    """Test that docs are accessible"""
    response = client.get("/docs")
    assert response.status_code == 200 