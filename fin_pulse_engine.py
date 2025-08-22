import streamlit as st
import yfinance as yf
import requests
import pandas as pd
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Fin-Pulse Engine - Credit Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Company mapping dictionary for popular Indian stocks
COMPANY_MAPPING = {
    'RELIANCE.NS': 'Reliance Industries',
    'TCS.NS': 'Tata Consultancy Services',
    'HDFCBANK.NS': 'HDFC Bank',
    'INFY.NS': 'Infosys',
    'ICICIBANK.NS': 'ICICI Bank',
    'HINDUNILVR.NS': 'Hindustan Unilever',
    'ITC.NS': 'ITC Limited',
    'SBIN.NS': 'State Bank of India',
    'BHARTIARTL.NS': 'Bharti Airtel',
    'KOTAKBANK.NS': 'Kotak Mahindra Bank',
    'LT.NS': 'Larsen & Toubro',
    'HCLTECH.NS': 'HCL Technologies',
    'ASIANPAINT.NS': 'Asian Paints',
    'MARUTI.NS': 'Maruti Suzuki',
    'TITAN.NS': 'Titan Company'
}

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_financial_data(ticker):
    """
    Fetch financial data for a given stock ticker using yfinance.
    
    Args:
        ticker (str): Stock ticker symbol
    
    Returns:
        dict or None: Dictionary with financial data or None if error
    """
    try:
        # Create ticker object and fetch info
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Check if ticker is valid
        if not info or len(info) < 3:  # Basic validation
            return None
        
        # Extract financial data with default values
        financial_data = {
            'ticker': ticker,
            'company_name': info.get('longName', info.get('shortName', 'Unknown')),
            'total_revenue': info.get('totalRevenue', 0),
            'total_debt': info.get('totalDebt', 0),
            'market_cap': info.get('marketCap', 0),
            'currency': info.get('currency', 'INR'),
            'sector': info.get('sector', 'Unknown'),
            'industry': info.get('industry', 'Unknown')
        }
        
        return financial_data
        
    except Exception as e:
        # Log error for debugging (in production, use proper logging)
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None

@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_news_headlines(company_name, api_key):
    """
    Fetch top 5 news headlines for a company using NewsAPI.
    
    Args:
        company_name (str): Name of the company
        api_key (str): NewsAPI key
    
    Returns:
        list: List of news headlines or empty list if error
    """
    try:
        # Check for placeholder API key
        if not api_key or api_key.strip() == "" or "placeholder" in api_key.lower():
            return []
        
        # NewsAPI endpoint
        url = "https://newsapi.org/v2/everything"
        
        # API parameters
        params = {
            'q': f'"{company_name}"',
            'sortBy': 'publishedAt',
            'pageSize': 5,
            'language': 'en',
            'apiKey': api_key
        }
        
        # Make API request
        response = requests.get(url, params=params, timeout=10)
        
        # Check response status
        if response.status_code != 200:
            return []
        
        data = response.json()
        
        # Validate response structure
        if data.get('status') != 'ok' or 'articles' not in data:
            return []
        
        articles = data.get('articles', [])
        if not articles:
            return []
        
        # Format headlines
        headlines = []
        for article in articles[:5]:
            headline = {
                'title': article.get('title', 'No title available'),
                'description': article.get('description', ''),
                'url': article.get('url', ''),
                'published_at': article.get('publishedAt', ''),
                'source': article.get('source', {}).get('name', 'Unknown')
            }
            headlines.append(headline)
        
        return headlines
        
    except Exception as e:
        print(f"Error fetching news for {company_name}: {str(e)}")
        return []

def calculate_credit_score(financial_data, news_headlines):
    """
    Calculate credit score based on financial data and news sentiment.
    
    Args:
        financial_data (dict or None): Financial data from yfinance
        news_headlines (list): List of news headlines
    
    Returns:
        tuple: (final_score, explanation_dict)
    """
    # Pre-check: Invalid ticker
    if financial_data is None:
        return 0, {
            'base_score': 0,
            'debt_ratio_impact': 0,
            'market_cap_impact': 0,
            'news_sentiment_impact': 0,
            'error': 'Invalid ticker or data unavailable'
        }
    
    # Initialize scoring
    base_score = 50
    current_score = base_score
    
    explanation = {
        'base_score': base_score,
        'debt_ratio_impact': 0,
        'market_cap_impact': 0,
        'news_sentiment_impact': 0
    }
    
    # 1. Debt-to-Revenue Ratio Analysis
    total_revenue = financial_data.get('total_revenue', 0)
    total_debt = financial_data.get('total_debt', 0)
    
    debt_ratio_impact = 0
    try:
        if total_revenue > 0 and total_debt >= 0:
            debt_ratio = total_debt / total_revenue
            
            # Scoring based on debt ratio
            if debt_ratio <= 0.2:
                debt_ratio_impact = 25  # Excellent
            elif debt_ratio <= 0.4:
                debt_ratio_impact = 15  # Good
            elif debt_ratio <= 0.6:
                debt_ratio_impact = 5   # Fair
            elif debt_ratio <= 0.8:
                debt_ratio_impact = -5  # Concerning
            elif debt_ratio <= 1.0:
                debt_ratio_impact = -15 # Poor
            else:
                debt_ratio_impact = -25 # Very Poor
                
            explanation['debt_ratio'] = round(debt_ratio, 3)
        else:
            # Penalize missing financial data
            debt_ratio_impact = -10
            explanation['debt_ratio'] = 'Data unavailable'
            
    except ZeroDivisionError:
        debt_ratio_impact = -20
        explanation['debt_ratio'] = 'Revenue is zero'
    
    explanation['debt_ratio_impact'] = debt_ratio_impact
    current_score += debt_ratio_impact
    
    # 2. Market Cap Analysis
    market_cap = financial_data.get('market_cap', 0)
    market_cap_impact = 0
    
    if market_cap > 0:
        # Convert to INR if needed (approximate)
        currency = financial_data.get('currency', 'INR')
        if currency == 'USD':
            market_cap_inr = market_cap * 83  # USD to INR
        else:
            market_cap_inr = market_cap
        
        # Award points based on market cap (in billions INR)
        market_cap_billions = market_cap_inr / 1_000_000_000
        
        if market_cap_billions >= 500:      # Large cap
            market_cap_impact = 20
        elif market_cap_billions >= 100:    # Mid-large cap
            market_cap_impact = 15
        elif market_cap_billions >= 50:     # Mid cap
            market_cap_impact = 10
        elif market_cap_billions >= 10:     # Small-mid cap
            market_cap_impact = 5
        else:                               # Small cap
            market_cap_impact = 0
        
        explanation['market_cap_billions'] = round(market_cap_billions, 2)
    else:
        explanation['market_cap_billions'] = 'Data unavailable'
    
    explanation['market_cap_impact'] = market_cap_impact
    current_score += market_cap_impact
    
    # 3. News Sentiment Analysis
    positive_keywords = [
        'profit', 'growth', 'deal', 'upgrade', 'surge', 'gain', 'rise',
        'expansion', 'acquisition', 'partnership', 'success', 'record',
        'strong', 'robust', 'positive', 'bullish', 'optimistic'
    ]
    
    negative_keywords = [
        'loss', 'fraud', 'scam', 'downgrade', 'slump', 'decline', 'fall',
        'crash', 'lawsuit', 'investigation', 'layoffs', 'crisis', 'warning',
        'deficit', 'trouble', 'concern', 'risk', 'scandal'
    ]
    
    news_sentiment_impact = 0
    positive_count = 0
    negative_count = 0
    
    if news_headlines:
        for headline in news_headlines:
            title = headline.get('title', '').lower()
            description = headline.get('description', '').lower()
            full_text = f"{title} {description}"
            
            # Check for sentiment keywords
            has_positive = any(keyword in full_text for keyword in positive_keywords)
            has_negative = any(keyword in full_text for keyword in negative_keywords)
            
            # Negative takes precedence
            if has_negative:
                negative_count += 1
                news_sentiment_impact -= 5
            elif has_positive:
                positive_count += 1
                news_sentiment_impact += 5
    
    explanation['news_sentiment_impact'] = news_sentiment_impact
    explanation['positive_news_count'] = positive_count
    explanation['negative_news_count'] = negative_count
    current_score += news_sentiment_impact
    
    # 4. Finalize score (clamp between 0-100)
    final_score = max(0, min(100, current_score))
    explanation['final_score'] = final_score
    
    return final_score, explanation

def generate_plain_language_summary(score, explanation, company_name):
    """
    Generate a plain-language summary of the credit analysis.
    
    Args:
        score (int): Final credit score (0-100)
        explanation (dict): Detailed score breakdown
        company_name (str): Name of the company
    
    Returns:
        str: Plain-language summary
    """
    # Get impact values
    debt_impact = explanation.get('debt_ratio_impact', 0)
    market_cap_impact = explanation.get('market_cap_impact', 0)
    news_impact = explanation.get('news_sentiment_impact', 0)
    
    # Determine overall assessment
    if score >= 80:
        overall = "shows excellent creditworthiness"
    elif score >= 65:
        overall = "demonstrates strong financial health"
    elif score >= 50:
        overall = "presents a moderate credit profile"
    elif score >= 35:
        overall = "shows concerning credit indicators"
    else:
        overall = "exhibits high credit risk"
    
    # Key strengths and concerns
    strengths = []
    concerns = []
    
    # Analyze debt position
    if debt_impact >= 15:
        strengths.append("excellent debt management")
    elif debt_impact >= 5:
        strengths.append("healthy debt levels")
    elif debt_impact <= -10:
        concerns.append("high debt burden")
    
    # Analyze market position
    if market_cap_impact >= 15:
        strengths.append("strong market position")
    elif market_cap_impact >= 10:
        strengths.append("solid market presence")
    elif market_cap_impact <= 5:
        concerns.append("limited market size")
    
    # Analyze news sentiment
    if news_impact >= 10:
        strengths.append("positive market sentiment")
    elif news_impact >= 5:
        strengths.append("favorable news coverage")
    elif news_impact <= -10:
        concerns.append("negative market sentiment")
    elif news_impact <= -5:
        concerns.append("mixed news sentiment")
    
    # Construct summary
    summary_parts = [f"Based on our comprehensive analysis, {company_name} {overall}."]
    
    if strengths:
        if len(strengths) == 1:
            summary_parts.append(f"The company benefits from {strengths[0]}.")
        else:
            summary_parts.append(f"Key strengths include {', '.join(strengths[:-1])}, and {strengths[-1]}.")
    
    if concerns:
        if len(concerns) == 1:
            if strengths:
                summary_parts.append(f"However, attention should be paid to {concerns[0]}.")
            else:
                summary_parts.append(f"Primary concerns include {concerns[0]}.")
        else:
            summary_parts.append(f"Areas of concern include {', '.join(concerns[:-1])}, and {concerns[-1]}.")
    
    # Add investment recommendation
    if score >= 75:
        summary_parts.append("This represents a solid investment-grade credit profile.")
    elif score >= 60:
        summary_parts.append("Overall, this indicates an acceptable credit risk for most investors.")
    elif score >= 40:
        summary_parts.append("Investors should carefully evaluate the risk-reward profile.")
    else:
        summary_parts.append("This credit profile suggests significant risk that requires careful consideration.")
    
    return " ".join(summary_parts)

def get_score_color(score):
    """Return color based on score for UI styling."""
    if score >= 80:
        return "green"
    elif score >= 60:
        return "orange"
    else:
        return "red"

def get_rating_category(score):
    """Convert score to rating category."""
    if score >= 85:
        return "AAA (Excellent)"
    elif score >= 75:
        return "AA (Very Good)"
    elif score >= 65:
        return "A (Good)"
    elif score >= 55:
        return "BBB (Fair)"
    elif score >= 45:
        return "BB (Below Average)"
    elif score >= 35:
        return "B (Poor)"
    else:
        return "C (High Risk)"

# Main Streamlit App
def main():
    # Header
    st.title("📊 Fin-Pulse Engine")
    st.markdown("### AI-Powered Credit Analysis for Indian Public Companies")
    st.markdown("Analyze the creditworthiness of publicly listed Indian companies using financial data and news sentiment.")
    
    # Sidebar for API key
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input(
            "NewsAPI Key (Optional)",
            type="password",
            help="Enter your NewsAPI key for news analysis. Leave empty to skip news analysis."
        )
        
        st.markdown("---")
        st.markdown("**Popular Tickers:**")
        for ticker, company in list(COMPANY_MAPPING.items())[:5]:
            st.code(f"{ticker} - {company}")
        
        with st.expander("View All Supported Companies"):
            for ticker, company in COMPANY_MAPPING.items():
                st.write(f"**{ticker}** - {company}")
    
    # Main input
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticker = st.text_input(
            "Enter Stock Ticker (e.g., TCS.NS, RELIANCE.NS)",
            placeholder="TCS.NS",
            help="Enter the NSE ticker symbol with .NS suffix"
        ).upper().strip()
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
        analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
    
    # Analysis execution
    if analyze_button and ticker:
        if not ticker.endswith('.NS'):
            st.warning("⚠️ Please add '.NS' suffix for Indian stocks (e.g., TCS.NS)")
            return
        
        with st.spinner('🔄 Fetching financial data and analyzing...'):
            # Get company name for news search
            company_name = COMPANY_MAPPING.get(ticker, ticker.replace('.NS', ''))
            
            # Fetch data
            financial_data = get_financial_data(ticker)
            news_headlines = get_news_headlines(company_name, api_key) if api_key else []
            
            # Calculate credit score
            score, explanation = calculate_credit_score(financial_data, news_headlines)
        
        # Display results
        if financial_data is None:
            st.error("❌ Invalid ticker or unable to fetch data. Please check the ticker symbol.")
            st.info("💡 Make sure to use the correct NSE format (e.g., TCS.NS, RELIANCE.NS)")
            return
        
        # Results layout
        st.markdown("---")
        st.subheader(f"📈 Analysis Results for {financial_data['company_name']}")
        
        # Main metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Credit Score",
                f"{score}/100",
                delta=f"{score-50:+d} from base",
                delta_color="normal"
            )
        
        with col2:
            rating = get_rating_category(score)
            rating_grade = rating.split()[0]  # e.g., "AAA"
            rating_desc = rating.split('(')[1].rstrip(')')  # e.g., "Excellent"
            st.metric(
                "Credit Rating", 
                rating_grade,
                delta=rating_desc,
                delta_color="off"
            )
        
        with col3:
            if financial_data['market_cap']:
                market_cap_cr = financial_data['market_cap'] / 10_000_000  # Convert to crores
                st.metric("Market Cap", f"₹{market_cap_cr:.0f}Cr")
            else:
                st.metric("Market Cap", "N/A")
        
        with col4:
            st.metric("Sector", financial_data.get('sector', 'Unknown'))
        
        # Generate and display plain language summary
        summary = generate_plain_language_summary(score, explanation, financial_data['company_name'])
        st.markdown("### 📝 Executive Summary")
        st.info(summary)
        
        # Detailed analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Score Breakdown")
            
            # Create breakdown data for chart
            breakdown_data = {
                'Component': ['Base Score', 'Debt Ratio', 'Market Cap', 'News Sentiment'],
                'Impact': [
                    explanation['base_score'],
                    explanation['debt_ratio_impact'],
                    explanation['market_cap_impact'],
                    explanation['news_sentiment_impact']
                ]
            }
            
            df_breakdown = pd.DataFrame(breakdown_data)
            st.bar_chart(df_breakdown.set_index('Component'))
            
            # Detailed explanation
            with st.expander("📋 Detailed Breakdown"):
                st.write(f"**Base Score:** {explanation['base_score']} points")
                st.write(f"**Debt Ratio Impact:** {explanation['debt_ratio_impact']:+d} points")
                if 'debt_ratio' in explanation:
                    st.write(f"  - Debt-to-Revenue Ratio: {explanation['debt_ratio']}")
                
                st.write(f"**Market Cap Impact:** {explanation['market_cap_impact']:+d} points")
                if 'market_cap_billions' in explanation:
                    st.write(f"  - Market Cap: ₹{explanation['market_cap_billions']} billion")
                
                st.write(f"**News Sentiment Impact:** {explanation['news_sentiment_impact']:+d} points")
                st.write(f"  - Positive News: {explanation.get('positive_news_count', 0)}")
                st.write(f"  - Negative News: {explanation.get('negative_news_count', 0)}")
        
        with col2:
            st.subheader("📰 Latest News Headlines")
            
            if news_headlines:
                for i, headline in enumerate(news_headlines, 1):
                    with st.expander(f"📄 {headline['title'][:80]}..."):
                        st.write(f"**Source:** {headline['source']}")
                        st.write(f"**Published:** {headline['published_at'][:10]}")
                        if headline['description']:
                            st.write(f"**Description:** {headline['description']}")
                        if headline['url']:
                            st.markdown(f"[Read full article]({headline['url']})")
            else:
                if not api_key:
                    st.info("🔑 Add NewsAPI key in sidebar to see news analysis")
                else:
                    st.warning("📰 No recent news found for this company")
        
        # Financial summary
        st.subheader("💰 Financial Summary")
        fin_col1, fin_col2, fin_col3 = st.columns(3)
        
        with fin_col1:
            revenue = financial_data.get('total_revenue', 0)
            if revenue:
                st.metric("Total Revenue", f"₹{revenue/10_000_000:.0f}Cr")
            else:
                st.metric("Total Revenue", "N/A")
        
        with fin_col2:
            debt = financial_data.get('total_debt', 0)
            if debt:
                st.metric("Total Debt", f"₹{debt/10_000_000:.0f}Cr")
            else:
                st.metric("Total Debt", "N/A")
        
        with fin_col3:
            if 'debt_ratio' in explanation and isinstance(explanation['debt_ratio'], float):
                st.metric("Debt-to-Revenue", f"{explanation['debt_ratio']:.2f}")
            else:
                st.metric("Debt-to-Revenue", "N/A")

    elif analyze_button and not ticker:
        st.warning("⚠️ Please enter a stock ticker symbol")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "💡 Fin-Pulse Engine - Built with Streamlit | "
        "Data powered by Yahoo Finance & NewsAPI"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()