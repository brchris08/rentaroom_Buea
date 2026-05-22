from fastapi.testclient import TestClient
from backend.main import app
import uuid

client = TestClient(app)

# Test 1 - Register a new user (random email to avoid duplicate error)
def test_register():
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@gmail.com"
    response = client.post("/auth/register", json={
        "full_name": "Test User",
        "email": unique_email,
        "password": "testpass123",
        "role": "student"
    })
    assert response.status_code == 200
    assert "user_id" in response.json()

# Test 2 - Login
def test_login():
    email = f"login_{uuid.uuid4().hex[:8]}@gmail.com"
    client.post("/auth/register", json={
        "full_name": "Login User",
        "email": email,
        "password": "testpass123",
        "role": "student"
    })
    response = client.post("/auth/login", json={
        "email": email,
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"

# Test 3 - Create a listing
def test_create_listing():
    response = client.post("/listings/", json={
        "title": "Test Room in Molyko",
        "neighborhood": "Molyko",
        "room_type": "Self Contain",
        "water": True,
        "electricity": True,
        "wifi": False,
        "price": 450000,
        "description": "Test description",
        "owner_id": 1
    })
    assert response.status_code == 200
    assert "listing_id" in response.json()

# Test 4 - Get all listings
def test_get_listings():
    response = client.get("/listings/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test 5 - Predict price (to be fixed once predict.py is shared)
def test_predict_price():
    response = client.post("/predict/", json={
        "neighborhood": "Molyko",
        "room_type": "Self Contain",
        "water": True,
        "electricity": True,
        "wifi": False,
        "actual_price" : 420000
    })
    assert response.status_code == 200
    assert "predicted_price" in response.json()