"""
Sentiment Analyzer Module

Handles AI-powered sentiment analysis using Google's Gemini API.
"""

import logging
import json
import time
from typing import List, Dict, Optional, Tuple
import google.generativeai as genai
from dataclasses import dataclass
from collections import Counter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SentimentResult:
    """Data class for sentiment analysis results."""
    sentiment: str 
    reasoning: str
    confidence: float
    article_title: str
    article_source: str

@dataclass
class SentimentReport:
    """Data class for final sentiment report."""
    overall_sentiment: str
    sentiment_breakdown: Dict[str, int]
    sentiment_percentages: Dict[str, float]
    bull_case: List[str]
    bear_case: List[str]
    total_articles: int
    analyzed_articles: int
    analysis_timestamp: str

class SentimentAnalyzer:
    """Handles sentiment analysis using Google's Gemini API."""
    
    def __init__(self, api_key: str):
        """
        Initialize the SentimentAnalyzer.
        
        Args:
            api_key: Google AI API key
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        self.last_request_time = 0
        self.min_request_interval = 5.0 
    
    def _rate_limit(self):
        """Implement rate limiting for API requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            logger.info(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def analyze_article_sentiment(self, article: Dict) -> Optional[SentimentResult]:
        """
        Analyze sentiment of a single news article.
        
        Args:
            article: Article data with title, description, content, etc.
            
        Returns:
            SentimentResult object or None if analysis fails
        """
        try:
            self._rate_limit()
            
            title = article.get('title', '')
            description = article.get('description', '')
            content = article.get('content', '')
            source = article.get('source', 'Unknown')
            
            full_text = f"Title: {title}\n\nDescription: {description}\n\nContent: {content}"
            
            prompt = self._create_analysis_prompt(full_text)
            
            logger.info(f"Analyzing article: {title[:50]}...")
            
            response = self.model.generate_content(prompt)
            
            if not response.text:
                logger.warning(f"No response generated for article: {title}")
                return None
            
            sentiment_data = self._parse_sentiment_response(response.text)
            
            if not sentiment_data:
                logger.warning(f"Could not parse sentiment for article: {title}")
                return None
            
            return SentimentResult(
                sentiment=sentiment_data['sentiment'],
                reasoning=sentiment_data['reasoning'],
                confidence=sentiment_data.get('confidence', 0.8),
                article_title=title,
                article_source=source
            )
            
        except Exception as e:
            logger.error(f"Error analyzing article sentiment: {str(e)}")
            return None
    
    def _create_analysis_prompt(self, article_text: str) -> str:
        """
        Create the prompt for article sentiment analysis.
        
        Args:
            article_text: Full text of the article to analyze
            
        Returns:
            Formatted prompt string
        """
        return f"""You are a senior financial analyst with expertise in market sentiment analysis. 
Analyze the following news article from an investor's perspective and determine its sentiment regarding the company.

Article Text:
{article_text}

Instructions:
1. Determine the overall sentiment as either "Positive", "Negative", or "Neutral"
2. Provide clear reasoning for your sentiment classification
3. Consider factors like:
   - Financial performance implications
   - Market impact potential
   - Strategic developments
   - Regulatory or competitive threats
   - Growth prospects
   - Risk factors

Return your analysis in the following JSON format:
{{
    "sentiment": "Positive/Negative/Neutral",
    "reasoning": "Detailed explanation of your sentiment analysis",
    "confidence": 0.85
}}

Be objective and focus on investment implications rather than general news sentiment."""

    def _parse_sentiment_response(self, response_text: str) -> Optional[Dict]:
        """
        Parse the sentiment analysis response from Gemini.
        
        Args:
            response_text: Raw response text from Gemini
            
        Returns:
            Parsed sentiment data or None if parsing fails
        """
        try:
            cleaned_text = response_text.strip()

            if '```json' in cleaned_text:
                json_start = cleaned_text.find('```json') + 7
                json_end = cleaned_text.find('```', json_start)
                json_text = cleaned_text[json_start:json_end].strip()
            elif '{' in cleaned_text and '}' in cleaned_text:
                json_start = cleaned_text.find('{')
                json_end = cleaned_text.rfind('}') + 1
                json_text = cleaned_text[json_start:json_end]
            else:
                logger.warning("No JSON found in response")
                return None
            
            sentiment_data = json.loads(json_text)
            
            if 'sentiment' not in sentiment_data or 'reasoning' not in sentiment_data:
                logger.warning("Missing required fields in sentiment response")
                return None

            sentiment = sentiment_data['sentiment'].strip().title()
            if sentiment not in ['Positive', 'Negative', 'Neutral']:
                logger.warning(f"Invalid sentiment value: {sentiment}")
                return None
            
            return {
                'sentiment': sentiment,
                'reasoning': sentiment_data['reasoning'].strip(),
                'confidence': sentiment_data.get('confidence', 0.8)
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error parsing sentiment response: {str(e)}")
            return None
    
    def generate_final_report(self, sentiment_results: List[SentimentResult], 
                            company_name: str) -> SentimentReport:
        """
        Generate final sentiment report from individual article analyses.
        
        Args:
            sentiment_results: List of SentimentResult objects
            company_name: Name of the company being analyzed
            
        Returns:
            SentimentReport object with comprehensive analysis
        """
        try:
            logger.info(f"Generating final report for {company_name}")
            
            if not sentiment_results:
                return self._create_empty_report(company_name)
            
            sentiments = [result.sentiment for result in sentiment_results]
            sentiment_counts = Counter(sentiments)
            
            total_articles = len(sentiment_results)
            sentiment_percentages = {
                sentiment: (count / total_articles) * 100 
                for sentiment, count in sentiment_counts.items()
            }
            
            overall_sentiment = self._determine_overall_sentiment(sentiment_percentages)
            
            bull_case, bear_case = self._generate_bull_bear_cases(sentiment_results, company_name)
            
            return SentimentReport(
                overall_sentiment=overall_sentiment,
                sentiment_breakdown=dict(sentiment_counts),
                sentiment_percentages=sentiment_percentages,
                bull_case=bull_case,
                bear_case=bear_case,
                total_articles=total_articles,
                analyzed_articles=len(sentiment_results),
                analysis_timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
            )
            
        except Exception as e:
            logger.error(f"Error generating final report: {str(e)}")
            return self._create_empty_report(company_name)
    
    def _determine_overall_sentiment(self, sentiment_percentages: Dict[str, float]) -> str:
        """
        Determine overall sentiment based on percentages.
        
        Args:
            sentiment_percentages: Dictionary of sentiment percentages
            
        Returns:
            Overall sentiment classification
        """
        max_sentiment = max(sentiment_percentages.items(), key=lambda x: x[1])
        
        if max_sentiment[1] < 40:
            return "Neutral"
        
        return max_sentiment[0]
    
    def _generate_bull_bear_cases(self, sentiment_results: List[SentimentResult], 
                                 company_name: str) -> Tuple[List[str], List[str]]:
        """
        Generate Bull and Bear case points from sentiment analysis.
        
        Args:
            sentiment_results: List of sentiment analysis results
            company_name: Name of the company
            
        Returns:
            Tuple of (bull_case_points, bear_case_points)
        """
        try:
            positive_reasoning = [
                result.reasoning for result in sentiment_results 
                if result.sentiment == 'Positive'
            ]
            negative_reasoning = [
                result.reasoning for result in sentiment_results 
                if result.sentiment == 'Negative'
            ]
            
            prompt = self._create_bull_bear_prompt(
                company_name, positive_reasoning, negative_reasoning
            )
            
            self._rate_limit()
            response = self.model.generate_content(prompt)
            
            if not response.text:
                return self._create_default_bull_bear_cases(sentiment_results)
            
            bull_bear_data = self._parse_bull_bear_response(response.text)
            
            if bull_bear_data:
                return bull_bear_data['bull_case'], bull_bear_data['bear_case']
            else:
                return self._create_default_bull_bear_cases(sentiment_results)
                
        except Exception as e:
            logger.error(f"Error generating Bull/Bear cases: {str(e)}")
            return self._create_default_bull_bear_cases(sentiment_results)
    
    def _create_bull_bear_prompt(self, company_name: str, positive_reasoning: List[str], 
                                negative_reasoning: List[str]) -> str:
        """Create prompt for Bull/Bear case generation."""
        return f"""You are a financial analyst summarizing market sentiment for {company_name}.

Based on the following sentiment analysis data, create a Bull Case and Bear Case:

POSITIVE REASONING (from positive sentiment articles):
{chr(10).join(f"- {reason}" for reason in positive_reasoning[:5])}

NEGATIVE REASONING (from negative sentiment articles):
{chr(10).join(f"- {reason}" for reason in negative_reasoning[:5])}

Instructions:
1. Create 3-5 compelling Bull Case points based on positive sentiment
2. Create 3-5 concerning Bear Case points based on negative sentiment
3. Focus on investment implications and market impact
4. Be specific and actionable
5. Use bullet points for clarity

Return in this JSON format:
{{
    "bull_case": [
        "Point 1 about positive developments",
        "Point 2 about growth opportunities",
        "Point 3 about competitive advantages"
    ],
    "bear_case": [
        "Point 1 about risks and challenges",
        "Point 2 about market concerns",
        "Point 3 about potential headwinds"
    ]
}}"""

    def _parse_bull_bear_response(self, response_text: str) -> Optional[Dict]:
        """Parse Bull/Bear case response from Gemini."""
        try:
            cleaned_text = response_text.strip()
            
            if '```json' in cleaned_text:
                json_start = cleaned_text.find('```json') + 7
                json_end = cleaned_text.find('```', json_start)
                json_text = cleaned_text[json_start:json_end].strip()
            elif '{' in cleaned_text and '}' in cleaned_text:
                json_start = cleaned_text.find('{')
                json_end = cleaned_text.rfind('}') + 1
                json_text = cleaned_text[json_start:json_end]
            else:
                return None
            
            return json.loads(json_text)
            
        except Exception as e:
            logger.error(f"Error parsing Bull/Bear response: {str(e)}")
            return None
    
    def _create_default_bull_bear_cases(self, sentiment_results: List[SentimentResult]) -> Tuple[List[str], List[str]]:
        """Create default Bull/Bear cases when AI generation fails."""
        bull_case = []
        bear_case = []
        
        for result in sentiment_results:
            if result.sentiment == 'Positive':
                bull_case.append(f"• {result.reasoning[:100]}...")
            elif result.sentiment == 'Negative':
                bear_case.append(f"• {result.reasoning[:100]}...")
        
        if not bull_case:
            bull_case = ["• Positive market sentiment detected in recent news"]
        if not bear_case:
            bear_case = ["• Some concerns identified in recent coverage"]
        
        return bull_case[:5], bear_case[:5]
    
    def _create_empty_report(self, company_name: str) -> SentimentReport:
        """Create an empty report when no data is available."""
        return SentimentReport(
            overall_sentiment="Neutral",
            sentiment_breakdown={"Neutral": 0},
            sentiment_percentages={"Neutral": 100.0},
            bull_case=["• No recent news available for analysis"],
            bear_case=["• No recent news available for analysis"],
            total_articles=0,
            analyzed_articles=0,
            analysis_timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
