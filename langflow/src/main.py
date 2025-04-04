import yfinance as yf
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI model
llm = ChatOpenAI(model_name="GPT-3.5", temperature=0)

# === Task Definitions ===
# Fetch stock data
def fetch_stock_data(symbol):
    """Retrieve historical stock data using yfinance."""
    stock = yf.Ticker(symbol)
    df = stock.history(period="1mo")  # Fetch last 1 month of data
    return df

def analyze_stock_data(stock_data: str):
    """
    Performs basic technical analysis (simulated).
    
    :param stock_data: Stock price history as a string.
    :return: Analysis results.
    """
    return f"📊 Technical analysis for given stock:\n- RSI: 55\n- MACD: Bullish Crossover\n- 50-day Moving Average: Above 200-day"

def generate_report(analysis: str):
    """
    Generates an AI-driven investment insights report.

    :param analysis: Results of stock analysis.
    :return: AI-generated financial report.
    """
    return f"📃 Investment Report:\n{analysis}\n📈 Recommendation: Consider for long-term investment."

# === LangChain Agent Tools ===
fetcher_tool = Tool(
    name="Stock Data Fetcher",
    func=fetch_stock_data,
    description="Fetch stock market data for a given ticker symbol."
)

analyst_tool = Tool(
    name="Stock Analyst",
    func=analyze_stock_data,
    description="Analyze stock trends, moving averages, RSI, and MACD."
)

reporter_tool = Tool(
    name="Investment Insights Generator",
    func=generate_report,
    description="Generate an investment report based on stock analysis."
)

# === Initialize LangChain Agent ===
tools = [fetcher_tool, analyst_tool, reporter_tool]
memory = ConversationBufferMemory(memory_key="chat_history")

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)

# === Execution ===
def run_analysis(symbol: str):
    """
    Runs the complete stock market analysis workflow.
    
    :param symbol: Stock ticker symbol.
    :return: Investment report.
    """
    print(f"\n🔍 Fetching data for {symbol}...")
    stock_data = fetch_stock_data(symbol)
    
    if "⚠️" in stock_data:
        return stock_data

    print("✅ Data fetched. Running analysis...")
    analysis = analyze_stock_data(stock_data)

    print("📊 Analysis complete! Generating investment report...")
    report = generate_report(analysis)

    return report

# === Main Execution ===
if __name__ == "__main__":
    result = run_analysis("AAPL")
    print(result)
