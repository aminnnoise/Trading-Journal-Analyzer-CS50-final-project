from project import build_query_str , double_sha256 , read_csv_
import pandas as pd

def test_build_query_str():
    params = {"b":2 , "a":1}
    assert build_query_str(params) == "a1b2"

def test_double_sha256():
    result = double_sha256("test")
    assert isinstance(result, str)
    assert len(result) == 64

def test_read_csv(tmp_path, monkeypatch):
    data = {
        "ctime": [1700000000000],
        "symbol": ["BTCUSDT"],
        "side": ["BUY"],
        "price": [30000],
        "qty": [1],
        "realizedPNL": [10],
        "fee": [0.5],
        "leverage": [10],
        "orderType": ["LIMIT"],
        "positionMode": ["ONE_WAY"],
    }

    df = pd.DataFrame(data)
    file = tmp_path / "bitunix_futures_trades.csv"
    df.to_csv(file, index=False)

    monkeypatch.chdir(tmp_path)

    total_trades, total_profit, total_fee, win_rate, best, worst, _ = read_csv_()

    assert total_trades == 1
    assert total_profit == 10
    assert total_fee == 0.5
    assert win_rate == 100.0
    assert best == 10
    assert worst == 10
