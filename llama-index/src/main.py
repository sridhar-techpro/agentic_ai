import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
import os
from openai import OpenAI as OpenAIClient  # Using openai directly instead of llama_index's wrapper

# Load environment variables
load_dotenv()

# Check for OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file. Please set it.")

# === Initialize LLM ===
llm = OpenAIClient(api_key=api_key)

# === Agent Definitions ===
class StockDataAgent:
    def fetch_stock_data(self, symbol: str) -> pd.DataFrame:
        """
        Fetches historical stock market data using Yahoo Finance.
        :param symbol: Stock ticker symbol (e.g., 'AAPL', 'TSLA').
        :return: Stock data as a Pandas DataFrame.
        """
        stock = yf.Ticker(symbol)
        return stock.history(period="1y")  # Changed to 1 year to ensure enough data for SMA_200

class StockAnalysisAgent:
    def analyze_stock_data(self, stock_data: pd.DataFrame) -> str:
        """
        Performs basic technical analysis on stock data.
        :param stock_data: Stock data DataFrame.
        :return: Analysis summary as a string.
        """
        if stock_data.empty:
            return "No stock data available."
        
        # Calculate Moving Averages
        stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()
        
        # Calculate RSI
        delta = stock_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        stock_data['RSI'] = 100 - (100 / (1 + rs))
        
        # Calculate MACD
        stock_data['EMA_12'] = stock_data['Close'].ewm(span=12, adjust=False).mean()
        stock_data['EMA_26'] = stock_data['Close'].ewm(span=26, adjust=False).mean()
        stock_data['MACD'] = stock_data['EMA_12'] - stock_data['EMA_26']
        stock_data['Signal_Line'] = stock_data['MACD'].ewm(span=9, adjust=False).mean()
        
        # Summary of latest values
        latest = stock_data.iloc[-1]
        summary = (
            f"Latest Close: ${latest['Close']:.2f}\n"
            f"SMA_50: ${latest['SMA_50']:.2f}, SMA_200: ${latest['SMA_200']:.2f}\n"
            f"RSI: {latest['RSI']:.2f}\n"
            f"MACD: {latest['MACD']:.2f}, Signal Line: {latest['Signal_Line']:.2f}"
        )
        return summary

class InvestmentAdvisorAgent:
    def __init__(self, llm):
        self.llm = llm
    
    def provide_insights(self, analysis: str) -> str:
        """
        Uses an LLM to generate investment insights based on analysis.
        :param analysis: Technical analysis summary.
        :return: AI-driven investment insights.
        """
        prompt = (
            "You are an investment advisor. Based on this stock analysis:\n"
            f"{analysis}\n"
            "Provide concise investment insights for a general audience."
        )
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()

# === Execution Pipeline ===
def run_analysis(symbol: str) -> str:
    """
    Runs the complete stock market analysis workflow using agents.
    :param symbol: Stock ticker symbol.
    :return: Final investment insights.
    """
    stock_agent = StockDataAgent()
    analysis_agent = StockAnalysisAgent()
    advisor_agent = InvestmentAdvisorAgent(llm)
    
    print(f"\n🔍 Fetching data for {symbol}...")
    stock_data = stock_agent.fetch_stock_data(symbol)
    
    if stock_data.empty:
        print("⚠️ No stock data found. Please check the ticker symbol.")
        return "❌ No data available."
    
    print("✅ Data fetched. Running analysis...")
    analysis = analysis_agent.analyze_stock_data(stock_data)
    
    print("📊 Analysis results:\n", analysis)
    print("🤖 Generating AI-driven investment insights...")
    insights = advisor_agent.provide_insights(analysis)
    
    print("📈 Analysis complete! Here are your investment insights:")
    return insights

# === Main Execution ===
if __name__ == "__main__":
    try:
        result = run_analysis("AAPL")
        print(result)
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")