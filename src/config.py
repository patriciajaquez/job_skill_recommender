"""
Configuration management for Job Market Intelligence Platform.
Centralized settings for Phase 2 implementation.
"""

import os
from pathlib import Path
from typing import Dict, Any

# Project structure
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
WORKFLOWS_DIR = PROJECT_ROOT / "workflows"

# Default configuration values
DEFAULT_CONFIG = {
    "api": {
        "request_timeout": 30,
        "retry_attempts": 3,
        "rate_limit_delay": 0.5
    },
    "data": {
        "cache_ttl": 1800,  # 30 minutes
        "max_cache_size": 1000,
        "quality_threshold": 0.8
    },
    "ml": {
        "model_cache_ttl": 7200,  # 2 hours
        "prediction_confidence_threshold": 0.7
    }
}

def get_config() -> Dict[str, Any]:
    """Get configuration with environment variable overrides."""
    config = DEFAULT_CONFIG.copy()
    
    # Override with environment variables if present
    if timeout := os.getenv("API_REQUEST_TIMEOUT"):
        config["api"]["request_timeout"] = int(timeout)
    
    if threshold := os.getenv("DATA_QUALITY_THRESHOLD"):
        config["data"]["quality_threshold"] = float(threshold)
    
    return config
