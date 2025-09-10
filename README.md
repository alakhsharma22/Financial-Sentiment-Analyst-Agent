# Financial Sentiment Analyst Agent

A comprehensive AI-powered tool for analyzing financial news sentiment and generating investor-focused reports. This application uses Google's Gemini AI to analyze recent news articles about companies and provides detailed sentiment breakdowns with Bull and Bear case analysis.

##  Features

- **AI-Powered Sentiment Analysis**: Uses Google's Gemini API for sophisticated financial sentiment analysis
- **Real-time News Fetching**: Retrieves recent news articles from NewsAPI.org
- **Company Data Integration**: Maps company names to stock tickers using yfinance
- **Professional Web Interface**: Clean, responsive Streamlit-based UI with interactive charts
- **Comprehensive Reporting**: Generates detailed Bull and Bear case analysis
- **Visual Analytics**: Interactive charts and graphs for sentiment visualization
- **Error Handling**: Robust error handling and user feedback
- **Rate Limiting**: Built-in API rate limiting to prevent quota exhaustion

##  Quick Start

### Prerequisites

- Python 3.9 or higher
- Google AI API key (for Gemini)
- NewsAPI.org API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Finance_agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API keys**
   
   **Option A: Environment Variables (Recommended)**
   ```bash
   export GOOGLE_AI_API_KEY="your_google_ai_api_key_here"
   export NEWS_API_KEY="your_news_api_key_here"
   ```

   **Option B: Direct Configuration**
   Edit `financial_agent/secrets.py` and replace the placeholder values with your actual API keys.

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501` to access the application.

##  Configuration

### API Keys Setup

#### Google AI API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Set the environment variable or update `secrets.py`

#### NewsAPI Key
1. Visit [NewsAPI.org](https://newsapi.org/register)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Set the environment variable or update `secrets.py`

### Application Settings

The application includes several configurable parameters accessible through the sidebar:

- **Days to look back**: Number of days to fetch news articles (1-30)
- **Maximum articles**: Limit on articles to analyze (5-50)
- **Analysis parameters**: Customizable for different use cases

##  Project Structure

```
financial_agent/
├── app.py                 # Main Streamlit application
├── data_fetcher.py        # News and company data fetching
├── analyzer.py            # LLM-powered sentiment analysis
├── secrets.py             # API keys storage
├── requirements.txt       # Dependencies
├── .gitignore            # Git ignore file
├── README.md             # Project documentation
└── test_data_fetch.py    # Testing script
```

##  Testing

Run the comprehensive test suite to validate all components:

```bash
python test_data_fetch.py
```

The test suite includes:
- API key validation
- Ticker symbol mapping
- News article fetching
- Company information retrieval
- Sentiment analysis
- Complete workflow testing

##  Usage Guide

### Basic Usage

1. **Enter Company Name**: Input the full company name or ticker symbol
2. **Configure Parameters**: Adjust analysis settings in the sidebar
3. **Run Analysis**: Click "Analyze Sentiment" to start the process
4. **View Results**: Review the comprehensive sentiment report

### Understanding the Results

#### Sentiment Breakdown
- **Positive**: Articles with optimistic outlook
- **Negative**: Articles highlighting concerns or risks
- **Neutral**: Articles with balanced or factual reporting

#### Bull Case
- Key positive developments
- Growth opportunities
- Competitive advantages
- Market catalysts

#### Bear Case
- Potential risks and challenges
- Market concerns
- Regulatory or competitive threats
- Headwinds and obstacles

##  Technical Details

### Architecture

The application follows a modular architecture with clear separation of concerns:

- **Data Layer**: `data_fetcher.py` handles all external API interactions
- **Analysis Layer**: `analyzer.py` manages AI-powered sentiment analysis
- **Presentation Layer**: `app.py` provides the user interface
- **Configuration Layer**: `secrets.py` manages API keys and settings

### AI Integration

The sentiment analysis uses Google's Gemini API with sophisticated prompt engineering:

- **Financial Context**: Prompts are tailored for investment analysis
- **Multi-factor Analysis**: Considers financial performance, market impact, and strategic developments
- **Confidence Scoring**: Provides confidence levels for each analysis
- **Rate Limiting**: Implements proper API rate limiting

### Data Sources

- **News**: NewsAPI.org for comprehensive news coverage
- **Company Data**: yfinance for ticker mapping and company information
- **AI Analysis**: Google Gemini for sentiment analysis

##  Development

### Code Quality

The project follows Python best practices:

- Type hints throughout
- Comprehensive docstrings
- Error handling and logging
- Modular design
- Clean code principles

### Adding Features

To extend the application:

1. **New Data Sources**: Add methods to `data_fetcher.py`
2. **Analysis Enhancements**: Extend `analyzer.py` with new analysis types
3. **UI Components**: Add new sections to `app.py`
4. **Configuration**: Update `secrets.py` for new settings

### Testing

```bash
python test_data_fetch.py

python -c "from test_data_fetch import test_ticker_mapping; test_ticker_mapping()"
```

##  Deployment

### Streamlit Community Cloud

1. Push your code to GitHub
2. Connect your repository to Streamlit Community Cloud
3. Set environment variables in the deployment settings
4. Deploy the application

### Local Production

1. Set up a production environment
2. Configure environment variables
3. Use a production WSGI server
4. Set up proper logging and monitoring

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

##  Performance Considerations

### API Rate Limits

- **Google AI**: 15 requests per minute (free tier)
- **NewsAPI**: 1000 requests per day (free tier)
- Built-in rate limiting prevents quota exhaustion

### Optimization Tips

- Limit the number of articles analyzed
- Use caching for repeated analyses
- Implement request batching where possible
- Monitor API usage and costs

##  Security

### API Key Management

- Never commit API keys to version control
- Use environment variables for production
- Rotate keys regularly
- Monitor API usage for anomalies

### Data Privacy

- No user data is stored permanently
- API keys are handled securely
- All data processing is done locally

##  Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify keys are correctly set
   - Check key permissions and quotas
   - Ensure keys are not expired

2. **No News Found**
   - Try different company names
   - Check date range settings
   - Verify NewsAPI key is working

3. **Analysis Failures**
   - Check Google AI API key
   - Verify internet connection
   - Review rate limiting settings

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

##  License

This project is for educational and analytical purposes only. It does not provide financial advice and should not be used as the sole basis for investment decisions.

##  Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

##  Support

For issues and questions:

1. Check the troubleshooting section
2. Review the test suite output
3. Check API key configuration
4. Review the logs for error details

##  Future Enhancements

Potential improvements and features:

- Historical sentiment tracking
- Multiple news source aggregation
- Export functionality for reports
- Dark/light theme toggle
- Real-time sentiment monitoring
- Portfolio-level sentiment analysis
- Integration with trading platforms
- Advanced charting and visualization
- Custom sentiment models
- Multi-language support

---

**Disclaimer**: This tool provides analytical insights only and should not be considered as financial advice. Always conduct your own research and consult with financial professionals before making investment decisions.
