"""
API Keys and Configuration Management

This module handles API key storage and configuration.
Priority: Environment variables > Direct configuration in this file
"""

import os
from typing import Optional

class Config:
    """Configuration class for API keys and settings."""
    
    def __init__(self):
        self.google_ai_api_key: Optional[str] = os.getenv('GOOGLE_AI_API_KEY')
        self.news_api_key: Optional[str] = os.getenv('NEWS_API_KEY')
        if not self.google_ai_api_key:
            self.google_ai_api_key = "//"  # Replace with your actual key
        if not self.news_api_key:
            self.news_api_key = "//"  # Replace with your actual key
    
    def validate_keys(self) -> bool:
        """Validate that all required API keys are set."""
        return (
            self.google_ai_api_key != "GEMINI_API" and
            self.news_api_key != "NEWS_API" and
            self.google_ai_api_key is not None and
            self.news_api_key is not None and
            len(self.google_ai_api_key) > 10 and  
            len(self.news_api_key) > 10
        )
    
    def get_key_status(self) -> dict:
        """Get the status of API keys for debugging."""
        return {
            'google_ai_configured': (
                self.google_ai_api_key != "GEMINI_API" and 
                self.google_ai_api_key is not None and 
                len(self.google_ai_api_key) > 10
            ),
            'news_api_configured': (
                self.news_api_key != "NEWS_API" and 
                self.news_api_key is not None and 
                len(self.news_api_key) > 10
            ),
            'google_ai_source': 'environment' if os.getenv('GOOGLE_AI_API_KEY') else 'secrets.py',
            'news_api_source': 'environment' if os.getenv('NEWS_API_KEY') else 'secrets.py'
        }

config = Config()