from fastapi.testclient import TestClient
from src.main import app
from tests.utils.report import generate_valid_report_request_json
from uuid import uuid4

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


def test_generate_report_empty_items():
    request_data = generate_valid_report_request_json()
    request_data["inventory_data"]["items"] = []  # Empty product list
    response = client.post("/reports/", json=request_data)
    assert response.status_code == 422
    assert "List should have at least 1 item after validation" in response.json()["detail"][0]["msg"]


def test_generate_report_negative_quantity():
    request_data = generate_valid_report_request_json()
    request_data["inventory_data"]["items"][0]["quantity"] = -5.0  # Negative quantity
    response = client.post("/reports/", json=request_data)
    assert response.status_code == 422
    assert "Input should be greater than or equal to 0" in response.json()["detail"][0]["msg"]


def test_generate_report_invalid_item_name():
    request_data = generate_valid_report_request_json()
    request_data["inventory_data"]["items"][0]["name"] = "A"  # Invalid product name
    response = client.post("/reports/", json=request_data)
    assert response.status_code == 422
    assert "String should have at least 3 characters" in str(response.json())


def test_get_report_not_found():
    report_id = "non-existent-id" # Invalid report ID
    response = client.get("/reports/" + report_id)
    assert response.status_code == 404
    assert response.json() == {"detail": f"Report with ID {report_id} not found."}


def generate_report(company_id: str, restaurant_id: str, name: str = "Test report name") -> str:
    """
    Helper function to create a report for testing purposes.
    """
    request_data = generate_valid_report_request_json()
    request_data["company_data"]["id"] = company_id
    request_data["restaurant_data"]["id"] = restaurant_id
    request_data["report_name"] = name
    
    response = client.post("/reports/", json=request_data)
    assert response.status_code == 200
    # Extract the generated report ID
    report_id = response.headers["Content-Disposition"].split("=")[1].replace(".pdf", "")
    return report_id


def test_list_reports_success():
    """
    Test listing reports with valid data and pagination.
    """
    # Create reports for different companies and restaurants
    company_id = str(uuid4())
    restaurant_id = str(uuid4())
    generate_report(company_id, restaurant_id)
    generate_report(company_id, restaurant_id)
    generate_report(company_id, str(uuid4()))  # Other restaurant
    generate_report(str(uuid4()), str(uuid4()))  # Other company and restaurant

    # List reports for the specific company and restaurant (the first ones)
    page_number = 1
    reports_per_page = 10
    response = client.get(f"/reports/?company_id={company_id}&restaurant_id={restaurant_id}&page={page_number}&per_page={reports_per_page}")
    assert response.status_code == 200

    response_data = response.json()
    assert len(response_data["reports"]) == response_data["total"] == 2
    assert response_data["page"] == page_number
    assert response_data["per_page"] == reports_per_page


def test_list_reports_no_reports_found():
    """
    Test listing reports for a non-existent company/restaurant combination.
    """
    # Random UUIDs for a non-existing combination
    non_existent_company = str(uuid4())
    non_existent_restaurant = str(uuid4())

    response = client.get(f"/reports/?company_id={non_existent_company}&restaurant_id={non_existent_restaurant}&page=1&per_page=12")
    assert response.status_code == 404
    assert response.json() == {"detail": "No reports found."}


def test_list_reports_invalid_page():
    """
    Test listing reports with a valid company/restaurant but an invalid page number.
    """
    # Create a single report
    company_id = str(uuid4())
    restaurant_id = str(uuid4())
    generate_report(company_id, restaurant_id)

    # Access a page out of range
    page_number = 99
    response = client.get(f"/reports/?company_id={company_id}&restaurant_id={restaurant_id}&page={page_number}&per_page=12")
    assert response.status_code == 400
    assert "out of range" in response.json()["detail"]


def test_download_report_success():
    # Create a report
    company_id = str(uuid4())
    restaurant_id = str(uuid4())
    report_id = generate_report(company_id, restaurant_id)

    # Download the report
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
    assert response.json() == {"detail": f"Report with ID {generated_uuid} not found."}
