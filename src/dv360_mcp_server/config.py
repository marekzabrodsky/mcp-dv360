"""Configuration management for DV360 MCP Server."""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """Configuration settings for DV360 MCP Server."""
    
    # Google API credentials
    google_application_credentials: Optional[str] = None
    oauth_client_id: Optional[str] = None
    oauth_client_secret: Optional[str] = None
    oauth_refresh_token: Optional[str] = None
    
    # DV360 API settings
    api_version: str = "v4"
    api_scope: str = "https://www.googleapis.com/auth/display-video"
    
    # Server settings
    log_level: str = "INFO"
    max_retries: int = 3
    timeout_seconds: int = 30
    
    def __post_init__(self):
        """Load configuration from environment variables."""
        self.google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.oauth_client_id = os.getenv("OAUTH_CLIENT_ID")
        self.oauth_client_secret = os.getenv("OAUTH_CLIENT_SECRET")  
        self.oauth_refresh_token = os.getenv("OAUTH_REFRESH_TOKEN")
        
        self.log_level = os.getenv("LOG_LEVEL", self.log_level)
        self.max_retries = int(os.getenv("MAX_RETRIES", self.max_retries))
        self.timeout_seconds = int(os.getenv("TIMEOUT_SECONDS", self.timeout_seconds))
    
    def validate(self) -> bool:
        """Validate that required configuration is present."""
        if self.google_application_credentials:
            return os.path.exists(self.google_application_credentials)
        
        return all([
            self.oauth_client_id,
            self.oauth_client_secret,
            self.oauth_refresh_token
        ])
    
    def get_credentials_type(self) -> str:
        """Determine which type of credentials are configured."""
        if self.google_application_credentials:
            return "service_account"
        elif self.oauth_client_id:
            return "oauth"
        return "none"