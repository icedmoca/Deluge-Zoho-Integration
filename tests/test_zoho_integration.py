"""
Unit tests for Zoho Books integration.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from src.zoho_integration import ZohoBooks, ZohoAuthError, ZohoAPIError
from src.config import ZohoConfig

@pytest.fixture
def mock_config():
    """Fixture providing a mock configuration."""
    return ZohoConfig(
        client_id="test_client_id",
        client_secret="test_client_secret",
        refresh_token="test_refresh_token",
        organization_id="test_org_id"
    )

@pytest.fixture
def zoho_books(mock_config):
    """Fixture providing a ZohoBooks instance with mocked config."""
    with patch('src.zoho_integration.get_config', return_value=mock_config):
        return ZohoBooks()

def test_token_expired_when_no_expiry_set(zoho_books):
    """Test that token is considered expired when no expiry is set."""
    assert zoho_books._token_expired is True

def test_token_expired_when_past_expiry(zoho_books):
    """Test that token is considered expired when past expiry time."""
    zoho_books._token_expires_at = datetime.now() - timedelta(minutes=5)
    assert zoho_books._token_expired is True

def test_token_not_expired_when_valid(zoho_books):
    """Test that token is not considered expired when within expiry time."""
    zoho_books._token_expires_at = datetime.now() + timedelta(minutes=5)
    assert zoho_books._token_expired is False

@patch('requests.post')
def test_refresh_access_token_success(mock_post, zoho_books):
    """Test successful access token refresh."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "access_token": "new_token",
        "expires_in": 3600
    }
    mock_post.return_value = mock_response
    
    zoho_books._refresh_access_token()
    
    assert zoho_books._access_token == "new_token"
    assert zoho_books._token_expires_at is not None

@patch('requests.post')
def test_refresh_access_token_failure(mock_post, zoho_books):
    """Test access token refresh failure."""
    mock_post.side_effect = Exception("API Error")
    
    with pytest.raises(ZohoAuthError):
        zoho_books._refresh_access_token()

@patch('requests.request')
def test_make_request_success(mock_request, zoho_books):
    """Test successful API request."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "test"}
    mock_request.return_value = mock_response
    
    zoho_books._access_token = "test_token"
    zoho_books._token_expires_at = datetime.now() + timedelta(hours=1)
    
    result = zoho_books._make_request("GET", "test_endpoint")
    assert result == {"data": "test"}

@patch('requests.request')
def test_make_request_failure(mock_request, zoho_books):
    """Test API request failure."""
    mock_request.side_effect = Exception("API Error")
    
    zoho_books._access_token = "test_token"
    zoho_books._token_expires_at = datetime.now() + timedelta(hours=1)
    
    with pytest.raises(ZohoAPIError):
        zoho_books._make_request("GET", "test_endpoint")

@patch.object(ZohoBooks, '_make_request')
def test_get_invoices_success(mock_make_request, zoho_books):
    """Test successful invoice retrieval."""
    mock_make_request.return_value = {
        "invoices": [
            {"id": "1", "amount": 100},
            {"id": "2", "amount": 200}
        ]
    }
    
    result = zoho_books.get_invoices(
        from_date="2024-01-01",
        to_date="2024-01-31",
        status="sent"
    )
    
    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[1]["amount"] == 200

@patch.object(ZohoBooks, '_make_request')
def test_get_invoices_empty_response(mock_make_request, zoho_books):
    """Test invoice retrieval with empty response."""
    mock_make_request.return_value = {}
    
    result = zoho_books.get_invoices()
    assert result == [] 