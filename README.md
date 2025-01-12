# SupplyWiseReporting

SupplyWiseReporting is a microservice designed to generate, list, and manage inventory reports for the SupplyWise application. Built with FastAPI and designed to run as an AWS Lambda function.

## 🚀 Technologies

- **FastAPI**: Modern, fast web framework for building APIs with Python
- **Mangum**: AWS Lambda integration for FastAPI
- **WeasyPrint**: PDF generation
- **Pydantic**: Data validation using Python type annotations
- **pytest**: Testing framework
- **boto3**: AWS SDK for Python, used for S3 integration
- **Python 3.12+**: Modern Python version with all its features

## 📋 Prerequisites

- Python 3.12 or higher
- pip (Python package installer)
- virtualenv or venv (recommended)
- AWS credentials (for production deployment)

## 🛠️ Local Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd SupplyWiseReporting
   ```

2. Create and activate a virtual environment:
   ```bash
   # Create virtual environment
   python3 -m venv venv

   # Activate on Linux/macOS
   source venv/bin/activate

   # Activate on Windows
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```bash
   uvicorn src.main:app --reload
   ```

The API will be available at `http://localhost:8000/docs`

## 🧪 Running Tests

- Ensure you're in the virtual environment and dependencies are installed:

1. Run tests:
   ```bash
   # Run all tests
   pytest tests/

   # Run specific test file
   pytest tests/test_routes.py
   ```

## 📄 License

[MIT License](LICENSE)
