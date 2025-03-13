"""
Configuration management for Zoho Books integration.
"""

import os
from typing import Optional
from pydantic import BaseSettings, SecretStr
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ZohoConfig(BaseSettings):
    """Zoho Books API configuration settings."""
    
    # Zoho OAuth credentials
    client_id: SecretStr
    client_secret: SecretStr
    refresh_token: SecretStr
    organization_id: str
    
    # API configuration
    api_base_url: str = "https://books.zoho.com/api/v3"
    auth_base_url: str = "https://accounts.zoho.com/oauth/v2"
    
    # Optional proxy configuration
    http_proxy: Optional[str] = None
    https_proxy: Optional[str] = None
    
    class Config:
        """Pydantic configuration class."""
        case_sensitive = False
        env_prefix = "ZOHO_"

def get_config() -> ZohoConfig:
    """
    Get the Zoho Books configuration.
    
    Returns:
        ZohoConfig: Configuration object with all necessary settings.
    
    Raises:
        ValueError: If required environment variables are missing.
    """
    try:
        return ZohoConfig()
    except Exception as e:
        raise ValueError(
            "Missing required environment variables. "
            "Please ensure all required ZOHO_* environment variables are set."
        ) from e 