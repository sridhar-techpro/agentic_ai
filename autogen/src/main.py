import os
import yfinance as yf
import numpy as np
# Manually define NaN if missing
if not hasattr(np, "NaN"):
    np.NaN = float("nan")
import pandas_ta as ta
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv
import logging

# Suppress unwanted logs
logging.getLogger("autogen").setLevel(logging.ERROR)

# Ensure np.NaN is defined
if not hasattr(np, "NaN"):
    np.NaN = float("nan")

# Load API keys from .env file
load_dotenv()

# Create AI Agents
def create_agents():
    """Create a multi-agent system for stock market analysis."""
    fetcher = AssistantAgent(
        name="DataFetcher",
        system_message="You fetch real-time and historical stock market data."
    )
    analyst = AssistantAgent(
        name="FinancialAnalyst",
        system_message="You analyze stock trends using moving averages, RSI, and MACD."
    )
    reporter = AssistantAgent(
        name="InvestmentReporter",
        system_message="You generate an investment report based on stock analysis."
    )
    return fetcher, analyst, reporter

# Fetch stock data
def fetch_stock_data(symbol):
    """Retrieve historical stock data using yfinance."""
    stock = yf.Ticker(symbol)
    df = stock.history(period="1mo")  # Fetch last 1 month of data
    return df

# Perform technical analysis
def analyze_stock_data(df):
    """Perform stock trend analysis using pandas_ta."""
    df["SMA_20"] = df["Close"].rolling(window=20).mean()  # 20-day SMA
    df["RSI"] = ta.rsi(df["Close"], length=14)  # RSI indicator
    return df

# Generate summary decision
def generate_summary(df, symbol):
    """Generate a buy/sell/hold decision based on RSI and SMA_20."""
    last_row = df.iloc[-1]  # Get latest stock data
    rsi = last_row["RSI"]
    sma_20 = last_row["SMA_20"]

    if np.isnan(rsi) or np.isnan(sma_20):
        return f"📌 Summary for {symbol}: Not enough data for decision."

    if rsi < 30:
        decision = "BUY 📈 (Stock is oversold, potential upside)"
    elif rsi > 70:
        decision = "SELL 📉 (Stock is overbought, potential downside)"
    else:
        decision = "HOLD ⚖️ (Stock is in a neutral range)"

    return f"📌 Summary for {symbol}: {decision}"

# Run multi-agent stock analysis
def run_analysis(symbol):
    """Orchestrates multi-agent execution for stock analysis."""
    fetcher, analyst, reporter = create_agents()
    config = {"use_docker": False}  # Disable Docker execution

    user_proxy = UserProxyAgent(
        name="Orchestrator", 
        human_input_mode="NEVER", 
        code_execution_config=config
    )

    # Step 1: Fetch Data
    stock_data = fetch_stock_data(symbol)
    fetcher.initiate_chat(user_proxy, message=f"Fetched stock data for {symbol}.", silent=True, max_turns=1)

    # Step 2: Analyze Data
    stock_data = analyze_stock_data(stock_data)
    analyst.initiate_chat(user_proxy, message=f"Performed analysis on {symbol} stock.", silent=True, max_turns=1)

    # Step 3: Generate Report
    final_report = f"📊 **Stock Analysis Report for {symbol}**\n\n{stock_data.tail()}\n\n"
    summary = generate_summary(stock_data, symbol)
    
    reporter.initiate_chat(user_proxy, message=final_report + summary, silent=True, max_turns=1)

    # Print only final summary
    return final_report + summary

# Run the script
if __name__ == "__main__":
    stock_symbol = "AAPL"
    report = run_analysis(stock_symbol)
    print(report)
