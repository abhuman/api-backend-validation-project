"""Pytest configuration and fixtures for API testing framework."""

import pytest
import requests
import os
import logging
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_tests.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def api_config():
    """Load API configuration from environment variables."""
    config = {
        'base_url': os.getenv('BASE_URL', 'https://api.example.com'),
        'timeout': int(os.getenv('TIMEOUT', '10')),
        'api_key': os.getenv('API_KEY', ''),
        'api_secret': os.getenv('API_SECRET', ''),
        'bearer_token': os.getenv('BEARER_TOKEN', ''),
        'environment': os.getenv('ENVIRONMENT', 'dev'),
        'report_dir': os.getenv('REPORT_DIR', 'reports'),
        'log_level': os.getenv('LOG_LEVEL', 'INFO')
    }
    logger.info(f"API configuration loaded for environment: {config['environment']}")
    return config


@pytest.fixture(scope="session")
def test_credentials():
    """Load test credentials from environment."""
    return {
        'username': os.getenv('TEST_USERNAME', 'test_user'),
        'password': os.getenv('TEST_PASSWORD', 'Test@123'),
        'email': os.getenv('TEST_EMAIL', 'test@example.com')
    }


@pytest.fixture(scope="function")
def api_session(api_config):
    """Create a requests session with default configuration."""
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })
    
    # Add authentication if available
    if api_config['bearer_token']:
        session.headers.update({
            'Authorization': f"Bearer {api_config['bearer_token']}"
        })
    elif api_config['api_key']:
        session.headers.update({
            'X-API-Key': api_config['api_key']
        })
    
    logger.info("API session created")
    yield session
    session.close()
    logger.info("API session closed")


@pytest.fixture(scope="function")
def api_client(api_config, api_session):
    """Create API client with base URL and session."""
    class APIClient:
        def __init__(self, base_url, session, timeout):
            self.base_url = base_url
            self.session = session
            self.timeout = timeout
        
        def get(self, endpoint, **kwargs):
            url = f"{self.base_url}{endpoint}"
            logger.info(f"GET {url}")
            response = self.session.get(url, timeout=self.timeout, **kwargs)
            logger.info(f"Response: {response.status_code}")
            return response
        
        def post(self, endpoint, **kwargs):
            url = f"{self.base_url}{endpoint}"
            logger.info(f"POST {url}")
            response = self.session.post(url, timeout=self.timeout, **kwargs)
            logger.info(f"Response: {response.status_code}")
            return response
        
        def put(self, endpoint, **kwargs):
            url = f"{self.base_url}{endpoint}"
            logger.info(f"PUT {url}")
            response = self.session.put(url, timeout=self.timeout, **kwargs)
            logger.info(f"Response: {response.status_code}")
            return response
        
        def delete(self, endpoint, **kwargs):
            url = f"{self.base_url}{endpoint}"
            logger.info(f"DELETE {url}")
            response = self.session.delete(url, timeout=self.timeout, **kwargs)
            logger.info(f"Response: {response.status_code}")
            return response
        
        def patch(self, endpoint, **kwargs):
            url = f"{self.base_url}{endpoint}"
            logger.info(f"PATCH {url}")
            response = self.session.patch(url, timeout=self.timeout, **kwargs)
            logger.info(f"Response: {response.status_code}")
            return response
    
    return APIClient(api_config['base_url'], api_session, api_config['timeout'])


@pytest.fixture(scope="function")
def valid_user_data(test_credentials):
    """Provide valid user test data."""
    return {
        "username": test_credentials['username'],
        "email": test_credentials['email'],
        "password": test_credentials['password']
    }


@pytest.fixture(scope="function")
def invalid_user_data():
    """Provide invalid user test data for negative testing."""
    return {
        "username": "",
        "email": "invalid-email",
        "password": "123"
    }


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "smoke: Smoke test suite")
    config.addinivalue_line("markers", "regression: Regression test suite")
    config.addinivalue_line("markers", "api: API endpoint tests")
    config.addinivalue_line("markers", "auth: Authentication tests")
    config.addinivalue_line("markers", "negative: Negative test cases")
    config.addinivalue_line("markers", "integration: Integration tests")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Log test results."""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        if report.passed:
            logger.info(f"✓ PASSED: {item.name}")
        elif report.failed:
            logger.error(f"✗ FAILED: {item.name}")
            logger.error(f"Error: {report.longreprtext}")
        elif report.skipped:
            logger.warning(f"⊘ SKIPPED: {item.name}")
