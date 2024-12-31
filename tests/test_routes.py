from fastapi.testclient import TestClient
from src.main import app
from tests.utils.report import generate_valid_report_request_json

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_report_success():
    request_data = generate_valid_report_request_json()
    response = client.post("/reports/", json=request_data)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "Content-Disposition" in response.headers


def test_generate_report_invalid_report_name():
    request_data = generate_valid_report_request_json()
    request_data["report_name"] = "a"  # Invalid name
    response = client.post("/reports/", json=request_data)
    assert response.status_code == 422
    assert "Report Name must be between 3 and 100 characters long" in str(response.json())


def test_generate_report_empty_products():
    request_data = generate_valid_report_request_json()
    request_data["inventory_data"]["products"] = []  # Empty product list
    response = client.post("/reports/", json=request_data)
    assert response.status_code == 422
    assert "List should have at least 1 item after validation" in response.json()["detail"][0]["msg"]


def test_generate_report_negative_quantity():
    request_data = generate_valid_report_request_json()
    request_data["inventory_data"]["products"][0]["quantity"] = -5.0  # Negative quantity
    response = client.post("/reports/", json=request_data)
    assert response.status_code == 422
    assert "Input should be greater than or equal to 0" in response.json()["detail"][0]["msg"]


def test_generate_report_invalid_product_name():
    request_data = generate_valid_report_request_json()
    request_data["inventory_data"]["products"][0]["name"] = "A"  # Invalid inventory name
    response = client.post("/reports/", json=request_data)
    assert response.status_code == 422
    assert "Item Name must be between 3 and 100 characters long" in str(response.json())


# def test_get_report_not_found():
#     response = client.get("/reports/non-existent-id")
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Report not found."}


# def test_list_reports_success():
#     # Create a report
#     request_data = generate_valid_report_request_json()
#     client.post("/reports/", json=request_data)

#     # List the metadata for the report
#     company_id = request_data["company_data"]["id"]
#     restaurant_id = request_data["restaurant_data"]["id"]
#     page_number = 1
#     items_per_page = 10
#     response = client.get(f"/reports/?company_id={company_id}&restaurant_id={restaurant_id}&page={page_number}&per_page={items_per_page}")

#     assert response.status_code == 200
#     response_data = response.json()
#     assert len(response_data["reports"]) == 1
#     assert response_data["page"] == page_number
#     assert response_data["per_page"] == items_per_page
#     assert response_data["total_reports"] == 1 # only 1 was created above
#     # assert "reports" in data
#     # assert len(data["reports"]) > 0
#     # assert data["total"] > 0
#     # assert data["page"] == 1
#     # assert data["per_page"] == 10


# def test_list_reports_no_reports_found():
#     # List reports from a non-existent combination of company and restaurant
#     response = client.get("/reports/?company_id=non-existent-company&restaurant_id=non-existent-restaurant&page=1&per_page=10")
#     assert response.status_code == 404
#     assert response.json() == {"detail": "No reports found."}


def test_download_report_success():
    # Create a report
    request_data = generate_valid_report_request_json()
    client.post("/reports/", json=request_data)

    # Download the report
    company_id = request_data["company_data"]["id"]
    restaurant_id = request_data["restaurant_data"]["id"]
    closing_time = request_data["inventory_data"]["actual_close_time"].split("T")[0]
    report_id = f"{company_id}-{restaurant_id}-{closing_time}"

    response = client.get(f"/reports/{report_id}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "Content-Disposition" in response.headers
    expected_filename = f'{report_id}.pdf'
    assert response.headers["Content-Disposition"] == f'attachment; filename="{expected_filename}"'

def test_download_report_not_found():
    generated_uuid = "00000000-0000-0000-0000-000000000000"
    response = client.get("/reports/" + generated_uuid)
    assert response.status_code == 404
    assert response.json() == {"detail": f"Report {generated_uuid} not found."}
