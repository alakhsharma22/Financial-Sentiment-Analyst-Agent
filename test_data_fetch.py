"""
Test script for data fetching functionality.

This script tests the data fetcher module to ensure all components
are working correctly before running the main application.
"""

import sys
import os
import logging
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from financial_agent.data_fetcher import DataFetcher
from financial_agent.analyzer import SentimentAnalyzer

def get_config():
    from financial_agent.secrets import Config
    return Config()

config = get_config()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_api_keys():
    """Test if API keys are properly configured."""
    print(" Testing API Key Configuration...")
    
    if not config.validate_keys():
        print(" API keys are not properly configured!")
        print("Please set the following environment variables:")
        print("- GOOGLE_AI_API_KEY")
        print("- NEWS_API_KEY")
        print("\nOr update the keys in financial_agent/secrets.py")
        return False
    
    print(" API keys are properly configured!")
    return True

def test_ticker_mapping():
    """Test ticker symbol mapping functionality."""
    print("\n Testing Ticker Symbol Mapping...")
    
    data_fetcher = DataFetcher(config.news_api_key)
    
    test_companies = [
        "Apple Inc.",
        "Microsoft Corporation",
        "Tata Motors",
        "Reliance Industries",
        "Tesla Inc."
    ]
    
    for company in test_companies:
        print(f"  Testing: {company}")
        ticker = data_fetcher.get_ticker(company)
        if ticker:
            print(f"     Found ticker: {ticker}")
        else:
            print(f"     No ticker found for {company}")
    
    return True

def test_news_fetching():
    """Test news article fetching functionality."""
    print("\n Testing News Article Fetching...")
    
    data_fetcher = DataFetcher(config.news_api_key)
    
    test_company = "Apple Inc."
    print(f"  Fetching news for: {test_company}")
    
    articles = data_fetcher.fetch_news_from_api(test_company, days_back=7)
    
    if articles:
        print(f"     Found {len(articles)} articles")
        
        if articles:
            first_article = articles[0]
            print(f"    Sample article:")
            print(f"      Title: {first_article.get('title', 'N/A')[:80]}...")
            print(f"      Source: {first_article.get('source', 'N/A')}")
            print(f"      Published: {first_article.get('publishedAt', 'N/A')}")
    else:
        print(f"     No articles found for {test_company}")
        return False
    
    return True

def test_company_info():
    """Test company information fetching."""
    print("\n Testing Company Information Fetching...")
    
    data_fetcher = DataFetcher(config.news_api_key)
    
    test_ticker = "AAPL"
    print(f"  Fetching company info for ticker: {test_ticker}")
    
    company_info = data_fetcher.get_company_info(test_ticker)
    
    if company_info:
        print(f"     Company info retrieved:")
        print(f"      Name: {company_info.get('name', 'N/A')}")
        print(f"      Sector: {company_info.get('sector', 'N/A')}")
        print(f"      Industry: {company_info.get('industry', 'N/A')}")
        print(f"      Market Cap: ${company_info.get('market_cap', 0):,}")
    else:
        print(f"     No company info found for {test_ticker}")
        return False
    
    return True

def test_sentiment_analysis():
    """Test sentiment analysis functionality."""
    print("\n Testing Sentiment Analysis...")
    
    analyzer = SentimentAnalyzer(config.google_ai_api_key)
    
    sample_article = {
        'title': 'Apple Reports Record Quarterly Revenue Growth',
        'description': 'Apple Inc. reported strong quarterly earnings with revenue exceeding expectations.',
        'content': 'Apple Inc. announced record quarterly revenue of $123.9 billion, representing a 8% increase year-over-year. The company saw strong growth across all product categories, with iPhone sales leading the way. CEO Tim Cook expressed optimism about future growth prospects.',
        'source': 'Financial Times',
        'url': 'https://example.com/article1',
        'publishedAt': '2024-01-15T10:00:00Z'
    }
    
    print("  Analyzing sample article...")
    result = analyzer.analyze_article_sentiment(sample_article)
    
    if result:
        print(f"      Sentiment analysis completed:")
        print(f"      Sentiment: {result.sentiment}")
        print(f"      Confidence: {result.confidence}")
        print(f"      Reasoning: {result.reasoning[:100]}...")
    else:
        print(f"     Sentiment analysis failed")
        return False
    
    return True

def test_full_workflow():
    """Test the complete workflow from company name to sentiment report."""
    print("\n Testing Complete Workflow...")
    
    data_fetcher = DataFetcher(config.news_api_key)
    analyzer = SentimentAnalyzer(config.google_ai_api_key)
    
    test_company = "Apple Inc."
    print(f"  Testing complete workflow for: {test_company}")
    
    print("    Step 1: Getting ticker symbol...")
    ticker = data_fetcher.get_ticker(test_company)
    if not ticker:
        print("     Failed to get ticker symbol")
        return False
    print(f"     Ticker found: {ticker}")
    
    print("    Step 2: Getting company information...")
    company_info = data_fetcher.get_company_info(ticker)
    if company_info:
        print(f"     Company info retrieved: {company_info.get('name', 'N/A')}")
    else:
        print("      Company info not available (continuing anyway)")
    
    print("    Step 3: Fetching news articles...")
    articles = data_fetcher.fetch_news_from_api(test_company, days_back=7)
    if not articles:
        print("     No news articles found")
        return False
    print(f"     Found {len(articles)} articles")
    
    print("    Step 4: Analyzing sentiment...")
    sentiment_results = []
    for i, article in enumerate(articles[:3]):  
        print(f"      Analyzing article {i+1}/{min(3, len(articles))}...")
        result = analyzer.analyze_article_sentiment(article)
        if result:
            sentiment_results.append(result)
    
    if not sentiment_results:
        print("     No sentiment analysis results")
        return False
    print(f"     Analyzed {len(sentiment_results)} articles")
    
    print("    Step 5: Generating final report...")
    report = analyzer.generate_final_report(sentiment_results, test_company)
    print(f"     Report generated:")
    print(f"      Overall Sentiment: {report.overall_sentiment}")
    print(f"      Sentiment Breakdown: {report.sentiment_breakdown}")
    print(f"      Bull Case Points: {len(report.bull_case)}")
    print(f"      Bear Case Points: {len(report.bear_case)}")
    
    return True

def main():
    """Run all tests."""
    print(" Financial Sentiment Analyst - Test Suite")
    print("=" * 50)
    
    tests = [
        ("API Key Configuration", test_api_keys),
        ("Ticker Symbol Mapping", test_ticker_mapping),
        ("News Article Fetching", test_news_fetching),
        ("Company Information", test_company_info),
        ("Sentiment Analysis", test_sentiment_analysis),
        ("Complete Workflow", test_full_workflow)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f" {test_name} - PASSED")
            else:
                print(f" {test_name} - FAILED")
        except Exception as e:
            print(f" {test_name} - ERROR: {str(e)}")
            logger.error(f"Test {test_name} failed with error: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print(" All tests passed! The system is ready to use.")
        return True
    else:
        print("  Some tests failed. Please check the configuration and try again.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
