"""Configuration for Okta MCP Server."""

import os
from typing import Optional
from pydantic import BaseModel, Field


class OktaConfig(BaseModel):
    """Okta MCP Server configuration."""

    org_url: str = Field(..., description="Okta organization URL")
    api_token: str = Field(..., description="Okta API token")
    concurrent_limit: int = Field(default=15, description="Maximum concurrent API requests")
    request_timeout: int = Field(default=30, description="API request timeout in seconds")
    max_retries: int = Field(default=1, description="Maximum retries on rate limit")

    @classmethod
    def from_env(cls) -> "OktaConfig":
        """Load configuration from environment variables."""
        org_url = os.getenv("OKTA_CLIENT_ORGURL")
        api_token = os.getenv("OKTA_API_TOKEN")

        if not org_url or not api_token:
            raise ValueError(
                "Okta configuration required. Set OKTA_CLIENT_ORGURL and OKTA_API_TOKEN environment variables."
            )

        return cls(
            org_url=org_url,
            api_token=api_token,
            concurrent_limit=int(os.getenv("OKTA_CONCURRENT_LIMIT", "15")),
            request_timeout=int(os.getenv("OKTA_REQUEST_TIMEOUT", "30")),
            max_retries=int(os.getenv("OKTA_MAX_RETRIES", "1")),
        )
