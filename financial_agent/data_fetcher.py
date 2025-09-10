"""
Data Fetcher Module

Handles fetching company data, news articles, and ticker symbol mapping.
"""

import logging
import requests
import yfinance as yf
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataFetcher:
    """Handles data fetching from various APIs and sources."""
    
    def __init__(self, news_api_key: str):
        """
        Initialize the DataFetcher.
        
        Args:
            news_api_key: NewsAPI.org API key
        """
        self.news_api_key = news_api_key
        self.news_base_url = "https://newsapi.org/v2/everything"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Financial-Sentiment-Analyst/1.0'
        })
    
    def get_ticker(self, company_name: str) -> Optional[str]:
        """
        Map company name to stock ticker symbol using yfinance.
        
        Args:
            company_name: Name of the company to search for
            
        Returns:
            Ticker symbol if found, None otherwise
        """
        try:
            logger.info(f"Searching for ticker symbol for: {company_name}")
            
            ticker = yf.Ticker(company_name)
            info = ticker.info
            
            if info and 'symbol' in info and info['symbol']:
                logger.info(f"Found ticker: {info['symbol']}")
                return info['symbol']
            
            variations = [
                company_name.upper(),
                company_name.replace(" ", ""),
                company_name.replace(" ", "."),
                company_name.replace(" ", "-"),
            ]
            
            for variation in variations:
                try:
                    ticker = yf.Ticker(variation)
                    info = ticker.info
                    if info and 'symbol' in info and info['symbol']:
                        logger.info(f"Found ticker with variation '{variation}': {info['symbol']}")
                        return info['symbol']
                except Exception:
                    continue
            
            logger.warning(f"Could not find ticker for: {company_name}")
            return None
            
        except Exception as e:
            logger.error(f"Error getting ticker for {company_name}: {str(e)}")
            return None
    
    def fetch_news_from_api(self, company_name: str, days_back: int = 5) -> List[Dict]:
        """
        Fetch recent news articles from NewsAPI.
        
        Args:
            company_name: Name of the company to fetch news for
            days_back: Number of days to look back for news
            
        Returns:
            List of news articles with relevant metadata
        """
        try:
            logger.info(f"Fetching news for: {company_name}")
            
            to_date = datetime.now()
            from_date = to_date - timedelta(days=days_back)
            
            params = {
                'q': f'"{company_name}"',
                'from': from_date.strftime('%Y-%m-%d'),
                'to': to_date.strftime('%Y-%m-%d'),
                'sortBy': 'publishedAt',
                'language': 'en',
                'pageSize': 50,
                'apiKey': self.news_api_key
            }
            
            response = self.session.get(self.news_base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'ok':
                logger.error(f"NewsAPI error: {data.get('message', 'Unknown error')}")
                return []
            
            articles = data.get('articles', [])
            logger.info(f"Fetched {len(articles)} articles for {company_name}")
            
            processed_articles = []
            for article in articles:
                if self._is_valid_article(article, company_name):
                    processed_articles.append({
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'content': article.get('content', ''),
                        'url': article.get('url', ''),
                        'publishedAt': article.get('publishedAt', ''),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'urlToImage': article.get('urlToImage', '')
                    })
            
            logger.info(f"Processed {len(processed_articles)} valid articles")
            return processed_articles
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching news: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error fetching news for {company_name}: {str(e)}")
            return []
    
    def _is_valid_article(self, article: Dict, company_name: str) -> bool:
        """
        Check if an article is valid and relevant.
        
        Args:
            article: Article data from NewsAPI
            company_name: Company name to check relevance against
            
        Returns:
            True if article is valid and relevant
        """
        if not article.get('title') or not article.get('description'):
            return False
        
        content = article.get('content', '')
        if len(content) < 100:
            return False
        
        text_to_check = f"{article.get('title', '')} {article.get('description', '')} {content}"
        company_lower = company_name.lower()
        text_lower = text_to_check.lower()
        
        return company_lower in text_lower
    
    def get_company_info(self, ticker: str) -> Optional[Dict]:
        """
        Get basic company information using yfinance.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with company information
        """
        try:
            logger.info(f"Fetching company info for ticker: {ticker}")
            
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.info
            
            if not info:
                logger.warning(f"No info found for ticker: {ticker}")
                return None
            
            company_info = {
                'symbol': info.get('symbol', ticker),
                'name': info.get('longName', info.get('shortName', 'Unknown')),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'market_cap': info.get('marketCap', 0),
                'current_price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'currency': info.get('currency', 'USD'),
                'country': info.get('country', 'Unknown'),
                'website': info.get('website', ''),
                'description': info.get('longBusinessSummary', '')
            }
            
            logger.info(f"Successfully fetched info for {company_info['name']}")
            return company_info
            
        except Exception as e:
            logger.error(f"Error fetching company info for {ticker}: {str(e)}")
            return None
