"""
===============================================================================
GCP SECRET MANAGER CLIENT FOR HEALTHCARE MULTI-AGENT PLATFORM
===============================================================================
Complies with HIPAA Security Rule by securely fetching sensitive keys
(Gemini API Key, Payer Gateway API Key, FHIR Store Token) directly from
Google Cloud Secret Manager at runtime without hardcoding in .env or containers.
===============================================================================
"""

import os
import time
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("GCP_Secret_Manager")


class GCPSecretManager:
    """Manages secure runtime retrieval and cached access to GCP Secret Manager."""
    
    _cache: Dict[str, Dict[str, Any]] = {}
    CACHE_TTL_SECONDS = 300  # 5-minute cache TTL

    @classmethod
    def get_secret(cls, secret_id: str, default: Optional[str] = None, version: str = "latest") -> str:
        """
        Retrieves a secret version string from GCP Secret Manager.
        Falls back to local environment variable if running locally or client unavailable.
        """
        now = time.time()
        
        # Check in-memory cache first to avoid redundant API latency
        if secret_id in cls._cache:
            entry = cls._cache[secret_id]
            if now - entry["timestamp"] < cls.CACHE_TTL_SECONDS:
                return entry["value"]

        project_id = os.getenv("GCP_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
        
        # Attempt to pull from GCP Secret Manager
        if project_id and os.getenv("USE_GCP_SECRET_MANAGER", "true").lower() == "true":
            try:
                from google.cloud import secretmanager
                client = secretmanager.SecretManagerServiceClient()
                name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
                
                logger.info(f"🔒 Fetching secret from GCP Secret Manager: {name}")
                response = client.access_secret_version(request={"name": name})
                secret_value = response.payload.data.decode("UTF-8").strip()
                
                # Cache secret
                cls._cache[secret_id] = {"value": secret_value, "timestamp": now}
                return secret_value
            except Exception as e:
                logger.warning(f"⚠️ Could not fetch '{secret_id}' from GCP Secret Manager ({e}). Checking environment variables.")

        # Fallback to local environment variable (e.g. during unit tests or local development)
        env_key = secret_id.upper().replace("-", "_")
        env_val = os.getenv(env_key, default)
        if env_val:
            cls._cache[secret_id] = {"value": env_val, "timestamp": now}
            return env_val

        return default or f"mock-secret-for-{secret_id}"

    @classmethod
    def get_gemini_api_key(cls) -> str:
        return cls.get_secret("gemini-api-key", default="mock-gemini-api-key")

    @classmethod
    def get_payer_api_gateway_key(cls) -> str:
        return cls.get_secret("payer-api-gateway-key", default="mock-payer-key-270-278")

    @classmethod
    def get_fhir_auth_token(cls) -> str:
        return cls.get_secret("fhir-auth-token", default="mock-fhir-token-r4")
