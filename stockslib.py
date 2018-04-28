import quandl

quandl.ApiConfig.api_key = '9zbEcC_ftQ4CEt3eq5iW'

sub_symbols_count = 60

def quandlFetch(symbols, date_from, date_to):
    columns = ['ticker', 'date', 'open', 'high', 'low', 'close']
    data = quandl.get_table('WIKI/PRICES', qopts = { 'columns': columns }, ticker = symbols, date = { 'gte': date_from, 'lte': date_to })
    
    tickers = data['ticker'].tolist()
    dates = data['date'].tolist()
    opens = data['open'].tolist()
    highs = data['high'].tolist()
    lows = data['low'].tolist()
    closes = data['close'].tolist()

    tickers_data = {}
    i = 0
    for ticker in tickers:
        if ticker not in tickers_data:
            tickers_data[ticker] = {'date':[], 'open':[], 'high':[], 'low':[], 'close':[]}
        tickers_data[ticker]['date'].append(dates[i])
        tickers_data[ticker]['open'].append(opens[i])
        tickers_data[ticker]['high'].append(highs[i])
        tickers_data[ticker]['low'].append(lows[i])
        tickers_data[ticker]['close'].append(closes[i])
        i += 1

    return tickers_data

def getQuandlBatchedData(symbols, date_from, date_to):
    batched_data =[]

    symbols_sub = []
    i = 0
    symbols_count = len(symbols)
    for symbol in symbols:
        symbols_sub.append(symbol)
        if (i+1) % sub_symbols_count == 0 or i == symbols_count-1:
            tickers_data = quandlFetch(symbols_sub, date_from, date_to)
            batched_data.append(tickers_data)

            symbols_sub = []

        i += 1

    return batched_data