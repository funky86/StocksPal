import datetime
import sqlite3
import stockslib

symbols = ['AAPL','NVDA']
date_from = '2018-01-01'
date_to = '2018-01-08'

conn = sqlite3.connect('stocks.db')
c = conn.cursor()

processed_tickers = []
batched_data = stockslib.getQuandlBatchedData(symbols, date_from, date_to)
for batch in batched_data:
    for ticker in batch:
        data = batch[ticker]
        v_ticker = ticker
        
        length = len(data['date'])
        for i in range(length):
            v_date = data['date'][i].date()
            v_open = data['open'][i]
            v_high = data['high'][i]
            v_low = data['low'][i]
            v_close = data['close'][i]

            # if symbol-date exists, exception will be thrown
            try:
                c.execute("INSERT INTO stocks (symbol, date, open, high, low, close) VALUES (?, ?, ?, ?, ?, ?)", (v_ticker, v_date, v_open, v_high, v_low, v_close))
                conn.commit()
            except:
                pass

conn.close()
