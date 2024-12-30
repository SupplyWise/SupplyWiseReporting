from fastapi.testclient import TestClient
from src.main import app
from tests.utils.report import generate_valid_report_request

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_generate_report_success():
    request_data = generate_valid_report_request()
    response = client.post("/reports/", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "report_id" in data
    assert "report_name" in data
    assert data["report_name"] == request_data["report_name"]

def test_generate_report_invalid_report_name():
    request_data = generate_valid_report_request()
    request_data["report_name"] = "a"  # Invalid name
    response = client.post("/reports/", json=request_data)
    assert response.status_code == 422
    assert "Report Name must be between 3 and 100 characters long" in str(response.json())

def test_generate_report_empty_products():
    request_data = generate_valid_report_request()
    request_data["products"] = []  # Empty products list
    response = client.post("/reports/", json=request_data)
    assert response.status_code == 422
    # Obtaining the pydantic error message
    assert "List should have at least 1 item after validation" in response.json()["detail"][0]["msg"]

def test_generate_report_negative_quantity():
    request_data = generate_valid_report_request()
    request_data["products"][0]["quantity"] = -5.0  # Negative quantity
    response = client.post("/reports/", json=request_data)
    assert response.status_code == 422
    # Obtaining the pydantic error message
    assert "Input should be greater than or equal to 0" in response.json()["detail"][0]["msg"]

def test_generate_report_invalid_product_name():
    request_data = generate_valid_report_request()
    request_data["products"][0]["name"] = "A"  # Nome inválido
    response = client.post("/reports/", json=request_data)
    assert response.status_code == 422
    assert "Item Name must be between 3 and 100 characters long" in str(response.json())

def test_get_report_not_found():
    response = client.get("/reports/non-existent-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Report not found."}
