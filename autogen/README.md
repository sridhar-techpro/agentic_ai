# AutoGen: Multi-Agent Stock Market Analysis System

🚀 A multi-agent AI system for stock market analysis and investment reporting, leveraging AutoGen, Yahoo Finance API, and Poetry for package management.

## 📌 Features

✅ Fetches real-time & historical stock data using `yfinance`
✅ Performs technical analysis (moving averages, RSI, MACD)
✅ Generates AI-driven investment insights & reports
✅ Modular and extensible with a multi-agent architecture

## 📚 Project Structure

```
autogen/
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
git clone https://github.com/your-repo/autogen.git
cd autogen
```

### 3️⃣ Create & Activate Virtual Environment

Poetry will automatically create a virtual environment in the project folder.

```sh
poetry install
```

To activate the environment:

```sh
poetry shell
```

## 🛠️ Usage

Run the AI-driven stock analysis with:

```sh
python src/main.py
```

Modify the stock ticker symbol in `main.py` to analyze different stocks.

## 🐜 Configuration (.env)

Create a `.env` file in the root directory to store environment variables if needed.

## 📦 Dependencies

Dependencies are managed via Poetry and defined in `pyproject.toml`:

- **AutoGen** (`autogen-openai>=0.2.7`)
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

