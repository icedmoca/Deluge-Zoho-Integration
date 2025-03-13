"""
Main module for Zoho Books integration with Deluge platform.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger

from .config import get_config, ZohoConfig

class ZohoAuthError(Exception):
    """Exception raised for authentication-related errors."""
    pass

class ZohoAPIError(Exception):
    """Exception raised for Zoho API-related errors."""
    pass

class ZohoBooks:
    """
    Zoho Books API integration class.
    
    This class handles all interactions with the Zoho Books API, including
    authentication and data retrieval.
    """
    
    def __init__(self):
        """Initialize the ZohoBooks integration with configuration."""
        self.config: ZohoConfig = get_config()
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
        
        # Configure logging
        logger.add(
            "zoho_integration.log",
            rotation="10 MB",
            retention="1 month",
            level="INFO"
        )
    
    @property
    def access_token(self) -> str:
        """
        Get a valid access token, refreshing if necessary.
        
        Returns:
            str: Valid access token for API requests.
        
        Raises:
            ZohoAuthError: If unable to obtain a valid access token.
        """
        if not self._access_token or self._token_expired:
            self._refresh_access_token()
        return self._access_token
    
    @property
    def _token_expired(self) -> bool:
        """Check if the current access token has expired."""
        if not self._token_expires_at:
            return True
        return datetime.now() >= self._token_expires_at
    
    def _refresh_access_token(self) -> None:
        """
        Refresh the access token using the refresh token.
        
        Raises:
            ZohoAuthError: If token refresh fails.
        """
        try:
            response = requests.post(
                f"{self.config.auth_base_url}/token",
                params={
                    "refresh_token": self.config.refresh_token.get_secret_value(),
                    "client_id": self.config.client_id.get_secret_value(),
                    "client_secret": self.config.client_secret.get_secret_value(),
                    "grant_type": "refresh_token"
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            self._access_token = data["access_token"]
            self._token_expires_at = datetime.now() + timedelta(
                seconds=data.get("expires_in", 3600)
            )
            
            logger.info("Successfully refreshed access token")
            
        except Exception as e:
            logger.error(f"Failed to refresh access token: {str(e)}")
            raise ZohoAuthError("Failed to refresh access token") from e
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Dict:
        """
        Make an authenticated request to the Zoho Books API.
        
        Args:
            method: HTTP method to use
            endpoint: API endpoint to call
            params: Optional query parameters
            data: Optional request body
            
        Returns:
            Dict containing the API response
            
        Raises:
            ZohoAPIError: If the API request fails
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
            
            url = f"{self.config.api_base_url}/{endpoint}"
            
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise ZohoAPIError(f"API request failed: {str(e)}") from e
    
    def get_invoices(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve invoices from Zoho Books.
        
        Args:
            from_date: Optional start date (YYYY-MM-DD)
            to_date: Optional end date (YYYY-MM-DD)
            status: Optional invoice status filter
            
        Returns:
            List of invoice dictionaries
        """
        params = {
            "organization_id": self.config.organization_id,
        }
        
        if from_date:
            params["date_start"] = from_date
        if to_date:
            params["date_end"] = to_date
        if status:
            params["status"] = status
            
        logger.info(f"Retrieving invoices with params: {params}")
        
        response = self._make_request(
            method="GET",
            endpoint="invoices",
            params=params
        )
        
        return response.get("invoices", []) 