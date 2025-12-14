import time
import os
import uuid
import hashlib
import requests
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

API_KEY = os.getenv("BITUNIX_API_KEY")
SECRET_KEY = os.getenv("BITUNIX_SECRET_KEY")
BASE_URL = "https://fapi.bitunix.com"
ENDPOINT = "/api/v1/futures/trade/get_history_trades"

def main():

    # Creating and maintaining csv files
    symbol = input("Enter your desired symbol: ")

    if not API_KEY or not SECRET_KEY:
        print("API keys not found. Skipping API request.")

    if API_KEY and SECRET_KEY:
        data = fetch_trade_history(symbol, limit=50)

        trade_list = data.get("data", {}).get("tradeList", [])
        if trade_list:
            df = pd.DataFrame(trade_list)
            df.to_csv("bitunix_futures_trades.csv", index=False)
            print("CSV file updated from API")
    else:
        print("Running in offline mode (CSV only)" )  

    total_trades , total_profit , total_fee , win_rate , best_trade , worst_trade , df = read_csv_()

    print("=== trading journal summary ===")
    print(f"Total trade : {total_trades}")
    print(f"Net profit/loss : {total_profit:+.2f} USDT")
    print(f"Total fees paid : {total_fee:.2f} USDT")
    print(f"Win Rate : {win_rate:.1f}%")
    print(f"best trade : +{best_trade:.2f} USDT")
    print(f"worst trade : {worst_trade:.2f} USDT")
    
    # Last 10 trades
    last_10_trade(df)   

    #monthly profit chart
    chart(df)


def build_query_str(params):
    parts = []
    for k in sorted(params.keys()):
        parts.append(f"{k}{params[k]}")
    return "".join(parts)

def double_sha256(s: str):
    # two layers of sha256
    d1 = hashlib.sha256(s.encode('utf-8')).hexdigest()
    d2 = hashlib.sha256((d1 + SECRET_KEY).encode('utf-8')).hexdigest()
    return d2

def fetch_trade_history(symbol="BTCUSDT", startTime=None, endTime=None, skip=0, limit=100):
    timestamp = str(int(time.time() * 1000))
    nonce = uuid.uuid4().hex

    #query parameters
    params = {
        "symbol": symbol,
        "skip": skip,
        "limit": limit,
        "timestamp": timestamp
    }
    
    # They will only be filled if the user enters a start/end value.
    if startTime: params["startTime"] = startTime
    if endTime: params["endTime"] = endTime

    # convert to sorted string
    query_str = build_query_str(params)

    # nonce + timestamp + apiKey + queryParams + body
    body_str = "" 
    digest_input = nonce + timestamp + API_KEY + query_str + body_str

    # sha256
    signature = double_sha256(digest_input)

    # Add sign to params
    params["sign"] = signature

    headers = {
        "api-key": API_KEY,
        "nonce": nonce,
        "timestamp": timestamp,
        "sign": signature,
        "language": "en-US",
        "Content-Type": "application/json"
    }

    url = BASE_URL + ENDPOINT
    r = requests.get(url, params=params, headers=headers)
    return r.json()

def read_csv_():
    df = pd.read_csv("bitunix_futures_trades.csv")
    cols = ['ctime', 'symbol', 'side', 'price', 'qty', 'realizedPNL', 'fee', 'leverage', 'orderType', 'positionMode']
    # converting timestamp (milliseconds) into understandable datetime
    df['ctime'] = pd.to_datetime(df['ctime'], unit='ms') 
    df['date'] = df['ctime'].dt.date
    df['month'] = df['ctime'].dt.to_period('M')
    df = df[cols].copy()
    # make sure profit/loss and fee are number
    df['realizedPNL'] = pd.to_numeric(df['realizedPNL'], errors='coerce').fillna(0)
    df['fee'] = pd.to_numeric(df['fee'], errors='coerce').fillna(0)

    # key performance metric
    total_trades = len(df)
    total_profit = df['realizedPNL'].sum()
    total_fee = df['fee'].sum()
    win_rate = (df['realizedPNL'] > 0).mean() * 100
    best_trade = df['realizedPNL'].max()
    worst_trade = df['realizedPNL'].min()

    return total_trades , total_profit , total_fee , win_rate , best_trade , worst_trade , df

def chart(df):    
    profit = []
    times = []
    for i in df['realizedPNL']:
        if i != 0 :
            profit.append(i)
    
    
    for j in df.itertuples():
        if j.realizedPNL != 0:
            times.append(str(j.ctime))
    
    plt.bar(times ,profit , color=['g' if x >= 0 else 'r' for x in profit])
    plt.axhline(0 , color="red" , linestyle = "--" )
    plt.xticks(rotation=45)
    plt.ylabel("USDT")
    plt.tight_layout()
    plt.show()

def last_10_trade(df):
    print("=== Last 10 Trades ===")
    last_10 = df.sort_values("ctime").head(10)

    table_data = last_10[[
        'ctime', 'symbol', 'side', 'price', 'realizedPNL', 'fee'
    ]].copy()

    # Format numbers nicely
    table_data['price'] = table_data['price'].apply(lambda x: f"{x:,.2f}")
    table_data['realizedPNL'] = table_data['realizedPNL'].apply(lambda x: f"{x:+.4f}")
    table_data['fee'] = table_data['fee'].apply(lambda x: f"{x:.4f}")
    table_data['ctime'] = table_data['ctime'].dt.strftime("%Y-%m-%d %H:%M")

    # Rename columns for beauty
    table_data.columns = ['Time', 'Symbol', 'Side', 'Price', 'P&L (USDT)', 'Fee']

    #    Print beautiful table
    print(tabulate(table_data, headers='keys', tablefmt='github', showindex=False))


if __name__ == "__main__":
    main()
