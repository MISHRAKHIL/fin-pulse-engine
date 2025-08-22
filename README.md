# 📊 Fin-Pulse Engine

**AI-Powered Credit Analysis for Indian Public Companies**

A sophisticated Streamlit web application that provides comprehensive credit analysis for publicly listed Indian companies using financial data and news sentiment analysis.

## 🚀 Features

### 💰 **Financial Analysis**
- **Credit Score Calculation**: AI-powered scoring system (0-100 scale)
- **Debt-to-Revenue Analysis**: Comprehensive debt ratio assessment
- **Market Cap Evaluation**: Company size and market position analysis
- **Real-time Data**: Live financial data from Yahoo Finance

### 📰 **News Sentiment Analysis**
- **Market Sentiment**: Integration with NewsAPI for real-time news
- **Keyword Analysis**: Positive/negative sentiment scoring
- **Latest Headlines**: Top 5 recent news articles per company

### 🏢 **Indian Stock Focus**
- **NSE Integration**: Pre-configured with popular Indian stocks
- **Company Mapping**: 15+ major Indian companies included
- **Local Currency**: INR-based financial calculations

### 📊 **Interactive Dashboard**
- **Beautiful UI**: Modern, responsive Streamlit interface
- **Visual Charts**: Score breakdown and financial metrics
- **Detailed Reports**: Comprehensive analysis explanations
- **Executive Summary**: Plain-language credit assessment

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project**
   ```bash
   # Navigate to your project directory
   cd "path/to/Akhil Project"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python -m streamlit run main.py
   ```

4. **Open in browser**
   - Navigate to: `http://localhost:8501`
   - The app will open automatically in your default browser

## 📋 Requirements

The following packages are automatically installed:

- **streamlit** (1.48.1) - Web application framework
- **yfinance** (0.2.65) - Yahoo Finance data integration
- **requests** - HTTP library for API calls
- **pandas** - Data manipulation and analysis

## 🎯 Usage Guide

### 1. **Access the Application**
- Open your web browser
- Go to `http://localhost:8501`
- The Fin-Pulse Engine dashboard will load

### 2. **Configure News API (Optional)**
- In the sidebar, enter your NewsAPI key
- This enables news sentiment analysis
- Leave empty to skip news features

### 3. **Analyze a Company**
- Enter a stock ticker (e.g., `TCS.NS`, `RELIANCE.NS`)
- **Important**: Use `.NS` suffix for Indian stocks
- Click the "🔍 Analyze" button

### 4. **Review Results**
- **Credit Score**: Overall rating (0-100)
- **Credit Rating**: Letter grade (AAA to C)
- **Financial Metrics**: Revenue, debt, market cap
- **Score Breakdown**: Detailed component analysis
- **News Headlines**: Recent company news (if API key provided)

## 🏢 Supported Companies

The application comes pre-configured with popular Indian stocks:

| Ticker | Company Name |
|--------|--------------|
| `RELIANCE.NS` | Reliance Industries |
| `TCS.NS` | Tata Consultancy Services |
| `HDFCBANK.NS` | HDFC Bank |
| `INFY.NS` | Infosys |
| `ICICIBANK.NS` | ICICI Bank |
| `HINDUNILVR.NS` | Hindustan Unilever |
| `ITC.NS` | ITC Limited |
| `SBIN.NS` | State Bank of India |
| `BHARTIARTL.NS` | Bharti Airtel |
| `KOTAKBANK.NS` | Kotak Mahindra Bank |
| `LT.NS` | Larsen & Toubro |
| `HCLTECH.NS` | HCL Technologies |
| `ASIANPAINT.NS` | Asian Paints |
| `MARUTI.NS` | Maruti Suzuki |
| `TITAN.NS` | Titan Company |

## 📊 Credit Scoring System

### **Score Ranges**
- **85-100**: AAA (Excellent) - Investment grade
- **75-84**: AA (Very Good) - Investment grade
- **65-74**: A (Good) - Investment grade
- **55-64**: BBB (Fair) - Investment grade
- **45-54**: BB (Below Average) - Speculative
- **35-44**: B (Poor) - Speculative
- **0-34**: C (High Risk) - Speculative

### **Scoring Components**
1. **Base Score**: 50 points (neutral starting point)
2. **Debt Ratio Impact**: ±25 points based on debt-to-revenue ratio
3. **Market Cap Impact**: ±20 points based on company size
4. **News Sentiment**: ±25 points based on recent news analysis

## 🔧 Configuration

### **NewsAPI Integration**
To enable news sentiment analysis:

1. **Get API Key**: Sign up at [NewsAPI.org](https://newsapi.org/)
2. **Enter Key**: Add your API key in the sidebar
3. **Restart**: The app will automatically detect and use the key

### **Customization**
- Modify `COMPANY_MAPPING` in `main.py` to add/remove companies
- Adjust scoring weights in `calculate_credit_score()` function
- Customize sentiment keywords for news analysis

## 🚨 Troubleshooting

### **Common Issues**

1. **"streamlit not recognized"**
   ```bash
   # Use this command instead:
   python -m streamlit run main.py
   ```

2. **Dependency conflicts**
   ```bash
   # Reinstall requirements:
   pip uninstall -r requirements.txt
   pip install -r requirements.txt
   ```

3. **Port already in use**
   ```bash
   # Kill process on port 8501:
   netstat -ano | findstr :8501
   taskkill /PID <PID> /F
   ```

4. **Invalid ticker error**
   - Ensure ticker ends with `.NS` for Indian stocks
   - Check spelling and format
   - Verify the stock is actively traded

### **Performance Tips**
- The app caches data for 5-10 minutes to improve performance
- News analysis is optional and can be skipped for faster results
- Use popular tickers for best data availability

## 📈 Technical Details

### **Architecture**
- **Frontend**: Streamlit web framework
- **Data Source**: Yahoo Finance API via yfinance
- **News API**: NewsAPI.org integration
- **Caching**: Built-in Streamlit caching for performance

### **Data Flow**
1. User inputs stock ticker
2. App fetches financial data from Yahoo Finance
3. Calculates credit score using proprietary algorithm
4. Fetches news data (if API key provided)
5. Generates comprehensive analysis report
6. Displays results in interactive dashboard

## 🤝 Contributing

Feel free to contribute to this project:

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Submit a pull request**

### **Areas for Improvement**
- Additional financial metrics
- More sophisticated sentiment analysis
- Historical trend analysis
- Export functionality
- Mobile app version

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Akhil Project** - Financial Technology Innovation

## 🙏 Acknowledgments

- **Yahoo Finance** for financial data
- **NewsAPI** for news integration
- **Streamlit** for the web framework
- **Open Source Community** for supporting libraries

---

**💡 Tip**: For the best experience, use a NewsAPI key to enable comprehensive news sentiment analysis and get the most accurate credit assessments.

**🚀 Ready to analyze?** Start the app and begin exploring Indian company credit profiles! 