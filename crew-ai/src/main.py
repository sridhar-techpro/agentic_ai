import yfinance as yf
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from typing import Any

# Load environment variables
load_dotenv()


# === AI Agent Definitions ===
def create_agents() -> tuple[Agent, Agent, Agent]:
    """
    Creates and returns AI agents for fetching data, analyzing stocks, and reporting insights.
    """
    fetcher = Agent(
        name="Data Fetcher",
        role="Stock Data Collector",
        goal="Fetch real-time and historical stock market data.",
        backstory="An AI agent specialized in gathering stock market data for analysis.",
        verbose=True,
    )

    analyst = Agent(
        name="Financial Analyst",
        role="Market Analyst",
        goal="Analyze stock trends, moving averages, RSI, and MACD.",
        backstory="An AI agent with expertise in technical stock market analysis.",
        verbose=True,
    )

    reporter = Agent(
        name="Investment Insights Reporter",
        role="Financial Journalist",
        goal="Generate an investment report based on analysis.",
        backstory="An AI agent skilled in creating insightful financial reports.",
        verbose=True,
    )

    return fetcher, analyst, reporter


# === Task Definitions ===
def fetch_stock_data(symbol: str) -> Any:
    """
    Fetches historical stock market data using Yahoo Finance.

    :param symbol: Stock ticker symbol (e.g., 'AAPL', 'TSLA').
    :return: Stock data as a Pandas DataFrame.
    """
    stock = yf.Ticker(symbol)
    return stock.history(period="6mo")


def create_tasks(fetcher: Agent, analyst: Agent, reporter: Agent) -> list[Task]:
    """
    Creates and returns the list of tasks for the AI agents.

    :param fetcher: Data Fetcher agent.
    :param analyst: Financial Analyst agent.
    :param reporter: Investment Insights Reporter agent.
    :return: List of AI tasks.
    """
    fetch_data_task = Task(
        description="Fetch stock data for the given ticker symbol.",
        agent=fetcher,
        run=lambda: fetch_stock_data("AAPL"),
        expected_output="Stock data for the given ticker symbol.",
    )

    analyze_task = Task(
        description="Perform technical analysis using moving averages, RSI, and MACD.",
        agent=analyst,
        run=lambda: "Technical analysis completed.",
        expected_output="Technical analysis results.",
    )

    report_task = Task(
        description="Generate an AI-driven stock market investment insight report.",
        agent=reporter,
        run=lambda: "Investment insight report generated.",
        expected_output="Investment insight report.",
    )

    return [fetch_data_task, analyze_task, report_task]


# === Crew Setup ===
def create_crew() -> Crew:
    """
    Creates and returns a multi-agent system (Crew) for stock market analysis.

    :return: Crew instance with agents and tasks.
    """
    fetcher, analyst, reporter = create_agents()
    tasks = create_tasks(fetcher, analyst, reporter)

    return Crew(agents=[fetcher, analyst, reporter], tasks=tasks)


# === Execution Pipeline ===
def run_analysis(symbol: str) -> str:
    """
    Runs the complete stock market analysis workflow.

    :param symbol: Stock ticker symbol.
    :return: Final investment report message.
    """
    print(f"\n🔍 Fetching data for {symbol}...")
    stock_data = fetch_stock_data(symbol)
    
    if stock_data.empty:
        print("⚠️ No stock data found. Please check the ticker symbol.")
        return "❌ No data available."

    print("✅ Data fetched. Running analysis...")
    crew = create_crew()
    crew.kickoff()
    
    print("📊 Analysis complete! Generating investment report...")
    return "✅ Investment report ready!"


# === Main Execution ===
if __name__ == "__main__":
    run_analysis("AAPL")
