# Trading-Journal-Analyzer-CS50-final-project
### Video Demo : <https://youtu.be/N8mddMwLXKA>

## Description
This project is a Python-based trading journal analyzer designed as the final project for CS50P.
It retrieves futures trading history from the Bitunix API, stores it in a CSV file, analyzes
key performance metrics, and presents both textual summaries and visual charts.

The program helps traders review their performance by calculating total profit/loss, win rate,
fees, best and worst trades, and displaying the most recent trades in a formatted table.

## Features
- Fetches futures trade history from the Bitunix API
- Saves trading data into a CSV file
- Analyzes key trading metrics:
  - Total trades
  - Net profit/loss
  - Total fees
  - Win rate
  - Best and worst trades
- Displays the last 10 trades in a formatted table
- Visualizes profit and loss using a bar chart
- Includes automated tests using pytest

## Installation

1. Clone the repository and navigate to the project directory.

2. Install dependencies using the requirements file:
```bash
pip install -r requirements.txt
```
## How to Run the Program
Run the program using:
```bash
python project.py
```

When the program starts:
 1. You will be prompted to enter a trading symbol (e.g. BTCUSDT).
 2. The program fetches recent futures trades from the Bitunix API.
 3. Trade data is saved to bitunix_futures_trades.csv.
 4. The program analyzes the CSV file.
 5. A trading summary is printed in the terminal.
 6. The last 10 trades are displayed in a formatted table.
 7. A profit/loss chart is shown.

## API Keys & Security
This project uses the Bitunix Futures API to fetch trading history data.
For security reasons, API keys are NOT hardcoded in the source code.

Instead, the program loads the API credentials from environment variables.

Required Environment Variables
Before running the program with live API access, set the following variables:
 • BITUNIX_API_KEY
 • BITUNIX_SECRET_KEY

## Windows(PowerShell)
```powershell
$env:BITUNIX_API_KEY="your_api_key_here"
$env:BITUNIX_SECRET_KEY="your_secret_key_here"
```
## macOS / Linux
```bash
export BITUNIX_API_KEY="your_api_key_here"
export BITUNIX_SECRET_KEY="your_secret_key_here"
```

## Offline Mode (No API Key Required)
If API keys are not provided, the program will automatically run in offline mode.

In this mode:
 • No API request is sent
 • The application reads trade data from the local CSV file
(bitunix_futures_trades.csv)
 • All analytics, summaries, tables, and charts still work normally

This allows the project to be safely reviewed and tested without exposing sensitive credentials.

## Why This Approach?
• Prevents accidental API key leaks
• Follows security best practices
• Allows easy testing and grading (e.g., for CS50 submission)
• Enables both online and offline usage

## Fiels
• project.py – Main program
• requirements.txt – Project dependencies
• bitunix_futures_trades.csv – Generated trade history
• test_project.py – Unit tests
• README.md – Project documentation

## Note
• This project is for educational purposes only.
• API keys are used for testing.
• Not financial advice.

## Author
Mohammad Amin Khobyari
CS50 python Final Project
