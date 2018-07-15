import sqlite3

def dbfetch(date_from, date_to, symbols):
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()

    rows = c.execute("SELECT symbol, date, open, high, low, close FROM stocks WHERE symbol=? ORDER BY symbol, date", symbols)

    tickers_data = {}
    for row in rows:
        ticker = row[0]
        if ticker not in tickers_data:
            tickers_data[ticker] = {'date':[], 'open':[], 'high':[], 'low':[], 'close':[]}
        tickers_data[ticker]['date'].append(row[1])
        tickers_data[ticker]['open'].append(row[2])
        tickers_data[ticker]['high'].append(row[3])
        tickers_data[ticker]['low'].append(row[4])
        tickers_data[ticker]['close'].append(row[5])

    conn.close()

    return tickers_data
