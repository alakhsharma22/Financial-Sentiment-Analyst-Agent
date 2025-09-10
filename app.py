"""
Financial Sentiment Analyst Agent - Main Streamlit Application

A comprehensive tool for analyzing financial news sentiment and generating
investor-focused reports using AI-powered analysis.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import logging
from typing import Optional, List, Dict

from financial_agent.data_fetcher import DataFetcher
from financial_agent.analyzer import SentimentAnalyzer, SentimentReport

def get_config():
    from financial_agent.secrets import Config
    return Config()

config = get_config()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Financial Sentiment Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .sentiment-positive {
        color: #28a745;
        font-weight: bold;
    }
    
    .sentiment-negative {
        color: #dc3545;
        font-weight: bold;
    }
    
    .sentiment-neutral {
        color: #ffc107;
        font-weight: bold;
    }
    
    .bull-case {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 5px 5px 0;
    }
    
    .bear-case {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 5px 5px 0;
    }
    
    .company-info {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
    
    .loading-spinner {
        text-align: center;
        padding: 2rem;
    }
    
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'current_company' not in st.session_state:
        st.session_state.current_company = None
    if 'sentiment_report' not in st.session_state:
        st.session_state.sentiment_report = None
    if 'company_info' not in st.session_state:
        st.session_state.company_info = None

def display_header():
    """Display the main application header."""
    st.markdown('<h1 class="main-header">📊 Financial Sentiment Analyst</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Market Sentiment Analysis for Smart Investment Decisions</p>', unsafe_allow_html=True)

def display_sidebar():
    """Display the sidebar with configuration options."""
    st.sidebar.header(" Configuration")
    
    if not config.validate_keys():
        st.sidebar.error(" API Keys Required")
        st.sidebar.markdown("""
        Please set the following environment variables:
        - `GOOGLE_AI_API_KEY`: Your Google AI API key
        - `NEWS_API_KEY`: Your NewsAPI.org key
        
        Or update the keys in `financial_agent/secrets.py`
        """)
        return False
    
    st.sidebar.success(" API Keys Configured")
    
    st.sidebar.subheader("📈 Analysis Parameters")
    
    days_back = st.sidebar.slider(
        "Days to look back for news",
        min_value=1,
        max_value=30,
        value=7,
        help="Number of days to fetch news articles from"
    )
    
    max_articles = st.sidebar.slider(
        "Maximum articles to analyze",
        min_value=1,
        max_value=10,
        value=5,
        help="Limit the number of articles to analyze (for faster processing)"
    )
    
    return {
        'days_back': days_back,
        'max_articles': max_articles
    }

def display_company_input():
    """Display the company input section."""
    st.header("🏢 Company Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        company_name = st.text_input(
            "Enter Company Name",
            placeholder="e.g., Tata Motors, Reliance Industries, Apple Inc.",
            help="Enter the full company name or ticker symbol"
        )
    
    with col2:
        analyze_button = st.button(
            "🔍 Analyze Sentiment",
            type="primary",
            use_container_width=True
        )
    
    return company_name, analyze_button

def display_loading_animation():
    """Display loading animation during analysis."""
    with st.spinner("Analyzing market sentiment..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            "🔍 Searching for company ticker...",
            "📰 Fetching recent news articles...",
            "🤖 Analyzing sentiment with AI...",
            "📊 Generating comprehensive report...",
            "✅ Analysis complete!"
        ]
        
        for i, step in enumerate(steps):
            progress_bar.progress((i + 1) / len(steps))
            status_text.text(step)
            time.sleep(0.5)
        
        progress_bar.empty()
        status_text.empty()

def display_company_info(company_info: Dict):
    """Display company information."""
    if not company_info:
        return
    
    st.markdown('<div class="company-info">', unsafe_allow_html=True)
    st.subheader("🏢 Company Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Company Name", company_info.get('name', 'N/A'))
        st.metric("Ticker Symbol", company_info.get('symbol', 'N/A'))
        st.metric("Sector", company_info.get('sector', 'N/A'))
    
    with col2:
        st.metric("Industry", company_info.get('industry', 'N/A'))
        st.metric("Country", company_info.get('country', 'N/A'))
        if company_info.get('market_cap'):
            market_cap = f"${company_info['market_cap']:,.0f}"
            st.metric("Market Cap", market_cap)
    
    with col3:
        if company_info.get('current_price'):
            price = f"${company_info['current_price']:.2f}"
            st.metric("Current Price", price)
        if company_info.get('website'):
            st.markdown(f"**Website:** [{company_info['website']}]({company_info['website']})")
    
    if company_info.get('description'):
        st.markdown("**Description:**")
        st.write(company_info['description'][:500] + "..." if len(company_info['description']) > 500 else company_info['description'])
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_sentiment_charts(report: SentimentReport):
    """Display sentiment analysis charts."""
    st.header("📊 Sentiment Analysis Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pie = px.pie(
            values=list(report.sentiment_breakdown.values()),
            names=list(report.sentiment_breakdown.keys()),
            title="Sentiment Distribution",
            color_discrete_map={
                'Positive': '#28a745',
                'Negative': '#dc3545',
                'Neutral': '#ffc107'
            }
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        sentiment_df = pd.DataFrame([
            {'Sentiment': k, 'Percentage': v} 
            for k, v in report.sentiment_percentages.items()
        ])
        
        fig_bar = px.bar(
            sentiment_df,
            x='Sentiment',
            y='Percentage',
            title="Sentiment Percentages",
            color='Sentiment',
            color_discrete_map={
                'Positive': '#28a745',
                'Negative': '#dc3545',
                'Neutral': '#ffc107'
            }
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    sentiment_class = report.overall_sentiment.lower()
    sentiment_emoji = {"positive": "📈", "negative": "📉", "neutral": "➡️"}
    
    st.markdown(f"""
    <div class="metric-card">
        <h2>Overall Sentiment: {sentiment_emoji.get(sentiment_class, '➡️')} {report.overall_sentiment}</h2>
        <p>Based on analysis of {report.analyzed_articles} articles</p>
    </div>
    """, unsafe_allow_html=True)

def display_bull_bear_cases(report: SentimentReport):
    """Display Bull and Bear case analysis."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="bull-case">', unsafe_allow_html=True)
        st.subheader("🐂 Bull Case")
        for point in report.bull_case:
            st.markdown(f"• {point}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="bear-case">', unsafe_allow_html=True)
        st.subheader("🐻 Bear Case")
        for point in report.bear_case:
            st.markdown(f"• {point}")
        st.markdown('</div>', unsafe_allow_html=True)

def display_analysis_details(report: SentimentReport):
    """Display detailed analysis information."""
    with st.expander("📋 Analysis Details", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Articles Found", report.total_articles)
        with col2:
            st.metric("Articles Analyzed", report.analyzed_articles)
        with col3:
            st.metric("Analysis Timestamp", report.analysis_timestamp)
        
        st.subheader("Detailed Sentiment Breakdown")
        sentiment_df = pd.DataFrame([
            {
                'Sentiment': sentiment,
                'Count': count,
                'Percentage': f"{percentage:.1f}%"
            }
            for sentiment, count in report.sentiment_breakdown.items()
            for percentage in [report.sentiment_percentages.get(sentiment, 0)]
        ])
        st.dataframe(sentiment_df, use_container_width=True)

def perform_analysis(company_name: str, config_params: Dict) -> tuple:
    """Perform the complete sentiment analysis."""
    try:
        data_fetcher = DataFetcher(config.news_api_key)
        analyzer = SentimentAnalyzer(config.google_ai_api_key)
        
        ticker = data_fetcher.get_ticker(company_name)
        if not ticker:
            return None, None, "Could not find ticker symbol for the given company name."
        
        company_info = data_fetcher.get_company_info(ticker)
        
        articles = data_fetcher.fetch_news_from_api(company_name, config_params['days_back'])
        if not articles:
            return company_info, None, "No recent news articles found for this company."

        articles = articles[:config_params['max_articles']]

        sentiment_results = []
        for i, article in enumerate(articles):
            result = analyzer.analyze_article_sentiment(article)
            if result:
                sentiment_results.append(result)
        
        if not sentiment_results:
            return company_info, None, "Could not analyze sentiment for any articles."
        
        report = analyzer.generate_final_report(sentiment_results, company_name)
        
        return company_info, report, None
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return None, None, f"Analysis failed: {str(e)}"

def main():
    """Main application function."""
    initialize_session_state()
    display_header()
    
    config_params = display_sidebar()
    if not config_params:
        st.stop()

    company_name, analyze_button = display_company_input()
    
    if analyze_button and company_name:
        if not company_name.strip():
            st.error("Please enter a company name.")
        else:
            display_loading_animation()
            
            company_info, report, error = perform_analysis(company_name.strip(), config_params)
            
            if error:
                st.error(f"❌ {error}")
            else:
                st.session_state.analysis_complete = True
                st.session_state.current_company = company_name.strip()
                st.session_state.sentiment_report = report
                st.session_state.company_info = company_info
                
                st.success("✅ Analysis completed successfully!")
    
    if st.session_state.analysis_complete and st.session_state.sentiment_report:
        st.markdown("---")
        
        if st.session_state.company_info:
            display_company_info(st.session_state.company_info)
        
        display_sentiment_charts(st.session_state.sentiment_report)
        
        display_bull_bear_cases(st.session_state.sentiment_report)
        
        display_analysis_details(st.session_state.sentiment_report)
        
        if st.button("🔄 Analyze Another Company", type="secondary"):
            st.session_state.analysis_complete = False
            st.session_state.current_company = None
            st.session_state.sentiment_report = None
            st.session_state.company_info = None
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>📊 Financial Sentiment Analyst | Powered by AI | For Educational Purposes Only</p>
        <p><em>This tool provides analytical insights only. Not financial advice.</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
