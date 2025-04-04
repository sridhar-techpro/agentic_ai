Langflow: Multi-Agent Stock Market Analysis System

🚀 A multi-agent AI system for stock market analysis and investment reporting, leveraging Langflow, Yahoo Finance API, and Poetry for package management.

📌 Features

✅ Fetches real-time &# Langflow: Multi-Agent Stock Market Analysis System

🚀 A multi-agent AI system for stock market analysis and investment reporting, leveraging **Langflow**, Yahoo Finance API, and Poetry for package management.

## 📌 Features

✅ Fetches real-time & historical stock data using `yfinance`  
✅ Performs technical analysis (moving averages, RSI, MACD)  
✅ Generates AI-driven investment insights & reports  
✅ Modular and extensible with a multi-agent architecture  
✅ **Langflow UI** for visual workflow management  

## 📚 Project Structure

```
langflow_stock_analysis/
│── src/
│   ├── __init__.py
│   ├── main.py
│── .env
│── poetry.lock
│── poetry.toml
│── pyproject.toml
│── README.md
```

## 🚀 Installation Guide

### 1️⃣ Install Poetry

If you haven't installed Poetry yet, run:

```sh
pip install poetry
```

Or, if using macOS/Linux, install via:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

### 2️⃣ Clone the Repository

```sh
git clone https://github.com/your-repo/langflow_stock_analysis.git
cd langflow_stock_analysis
```

### 3️⃣ Install Dependencies

Poetry will automatically create a virtual environment and install dependencies.

```sh
poetry install
```

### 4️⃣ Run Langflow

To start the **Langflow UI** for managing the agentic workflow, run:

```sh
poetry run langflow run
```

Then open your browser and go to **http://localhost:7860** to access Langflow.

## 🛠️ Setting Up the Stock Analysis Flow in Langflow

1. **Add a ChatOpenAI Block** (for AI-powered responses)
2. **Add a Memory Block** (for conversation history)
3. **Create Three Tools in Langflow**:
   - **Stock Data Fetcher** → Fetches stock data using `yfinance`
   - **Stock Analyst** → Performs technical analysis (moving averages, RSI, MACD)
   - **Investment Insights Generator** → Generates reports based on analysis
4. **Chain These Tools Together** to create a **LangChain agent**
5. **Deploy & Test** by running a stock ticker query!

## 🐜 Configuration (.env)

Create a `.env` file in the root directory to store API keys or environment variables if needed.

## 📦 Dependencies

Dependencies are managed via Poetry and defined in `pyproject.toml`:

- **Langflow** (`langflow>=0.2.0`)
- **LangChain** (`langchain>=0.1.0`)
- **Yahoo Finance API** (`yfinance>=0.2.55`)
- **Pandas TA** (`pandas-ta<0.3.0`)
- **Dotenv** (`python-dotenv>=1.1.0`)

To add more dependencies:

```sh
poetry add <package-name>
```

## 🛡️ License

This project is licensed under the **MIT License**.

## 🤝 Contributing

Feel free to submit issues, pull requests, or suggestions to improve this project!
 historical stock data using yfinance
✅ Performs technical analysis (moving averages, RSI, MACD)
✅ Generates AI-driven investment insights & reports
✅ Modular and extensible with a multi-agent architecture
✅ Langflow UI for visual workflow management

📚 Project Structure

langflow_stock_analysis/
│── src/
│   ├── __init__.py
│   ├── main.py
│── .env
│── poetry.lock
│── poetry.toml
│── pyproject.toml
│── README.md

🚀 Installation Guide

1️⃣ Install Poetry

If you haven't installed Poetry yet, run:

pip install poetry

Or, if using macOS/Linux, install via:

curl -sSL https://install.python-poetry.org | python3 -

2️⃣ Clone the Repository

git clone https://github.com/your-repo/langflow_stock_analysis.git
cd langflow_stock_analysis

3️⃣ Install Dependencies

Poetry will automatically create a virtual environment and install dependencies.

poetry install

4️⃣ Run Langflow

To start the Langflow UI for managing the agentic workflow, run:

poetry run langflow run

Then open your browser and go to http://localhost:7860 to access Langflow.

🛠️ Setting Up the Stock Analysis Flow in Langflow

Add a ChatOpenAI Block (for AI-powered responses)

Add a Memory Block (for conversation history)

Create Three Tools in Langflow:

Stock Data Fetcher → Fetches stock data using yfinance

Stock Analyst → Performs technical analysis (moving averages, RSI, MACD)

Investment Insights Generator → Generates reports based on analysis

Chain These Tools Together to create a LangChain agent

Deploy & Test by running a stock ticker query!

🐜 Configuration (.env)

Create a .env file in the root directory to store API keys or environment variables if needed.

📦 Dependencies

Dependencies are managed via Poetry and defined in pyproject.toml:

Langflow (langflow>=0.2.0)

LangChain (langchain>=0.1.0)

Yahoo Finance API (yfinance>=0.2.55)

Pandas TA (pandas-ta<0.3.0)

Dotenv (python-dotenv>=1.1.0)

To add more dependencies:

poetry add <package-name>

🛡️ License

This project is licensed under the MIT License.

🤝 Contributing

Feel free to submit issues, pull requests, or suggestions to improve this project!