"""
Example configuration file for Financial Sentiment Analyst Agent

Copy this file to config.py and update with your actual values.
"""

GOOGLE_AI_API_KEY = "//"
NEWS_API_KEY = "//"

ANALYSIS_DAYS_BACK = 7  
MAX_ARTICLES = 20      
RATE_LIMIT_DELAY = 1.0  

DEFAULT_THEME = "light"  
CHART_COLORS = {
    'positive': '#28a745',
    'negative': '#dc3545',
    'neutral': '#ffc107'
}

LOG_LEVEL = "INFO"  
LOG_FILE = "financial_agent.log"


ENABLE_CACHE = True
CACHE_TTL = 3600  
