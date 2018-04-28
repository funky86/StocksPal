import quandl
import datetime
 
quandl.ApiConfig.api_key = '9zbEcC_ftQ4CEt3eq5iW'

symbols = ['AAPL','NVDA']
date_from = '2018-01-01'
date_to = '2018-01-05'

def quandlFetch(symbols, date_from, date_to):
    columns = ['ticker', 'date', 'open', 'high', 'low', 'close']
    data = quandl.get_table('WIKI/PRICES', qopts = { 'columns': columns }, ticker = symbols, date = { 'gte': date_from, 'lte': date_to })
    
    tickers = data['ticker'].tolist()
    opens = data['open'].tolist()
    highs = data['high'].tolist()
    lows = data['low'].tolist()
    closes = data['close'].tolist()

    tickers_data = {}
    i = 0
    for ticker in tickers:
        if ticker not in tickers_data:
            tickers_data[ticker] = {'open':[], 'high':[], 'low':[], 'close':[]}
        tickers_data[ticker]['open'].append(opens[i])
        tickers_data[ticker]['high'].append(highs[i])
        tickers_data[ticker]['low'].append(lows[i])
        tickers_data[ticker]['close'].append(closes[i])
        i += 1

    return tickers_data

data = quandlFetch(symbols, date_from, date_to)
print(data)
