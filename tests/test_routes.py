from fastapi.testclient import TestClient
from src.main import app
from uuid import uuid4

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_generate_report_success():
    response = client.post(
        "/reports/",
        json={
            "company_id": str(uuid4()),
            "company_name": "Test Company",
            "restaurant_id": str(uuid4()),
            "restaurant_name": "Test Restaurant",
            "user_id": str(uuid4()),
            "user_name": "Test User",
            "inventory_close_time": "2024-12-22T10:00:00",
            "products": [
                {"product_id": str(uuid4()), "product_name": "Product A", "quantity": 5.0},
                {"product_id": str(uuid4()), "product_name": "Product B", "quantity": 10.0}
            ],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "report_id" in data
    assert data["report_id"].startswith("2024-12-22")

def test_generate_report_empty_products():
    response = client.post(
        "/reports/",
        json={
            "company_id": str(uuid4()),
            "company_name": "Test Company",
            "restaurant_id": str(uuid4()),
            "restaurant_name": "Test Restaurant",
            "user_id": str(uuid4()),
            "user_name": "Test User",
            "inventory_close_time": "2024-12-22T10:00:00",
            "products": [],
        },
    )
    assert response.status_code == 422  # Validation error
    assert "Products list must not be empty" in response.json()["detail"][0]["msg"]

def test_generate_report_negative_quantity():
    response = client.post(
        "/reports/",
        json={
            "company_id": str(uuid4()),
            "company_name": "Test Company",
            "restaurant_id": str(uuid4()),
            "restaurant_name": "Test Restaurant",
            "user_id": str(uuid4()),
            "user_name": "Test User",
            "inventory_close_time": "2024-12-22T10:00:00",
            "products": [
                {"product_id": str(uuid4()), "product_name": "Product A", "quantity": -5.0}
            ],
        },
    )
    assert response.status_code == 422  # Validation error
    assert "Quantity must be non-negative" in response.json()["detail"][0]["msg"]

def test_get_report_not_found():
    response = client.get("/reports/non-existent-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Report not found."}
