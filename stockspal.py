from datetime import datetime, timedelta
from mpl_finance import candlestick2_ohlc

import matplotlib.pyplot as plt
import quandl
import stockslib

def getMva(input, length):
    i = len(input)-1
    values = [[],[],{}]
    while i >= length-1:
        pos = i
        sum = 0
        count = 0
        while count < length:
            sum = sum + input[pos-count]
            count = count+1
        avg = sum/count
        values[0].append(i)  # x value
        values[1].append(avg)  # y value
        values[2][i] = avg  # y value mapped by x (represents the key)
        i = i-1
    return values

# 78% bullish reversal
def isMorningStar(open1, close1, open2, close2, open3, close3):
    return open1 > close1 and open2 < close1 and open2 < open3 and open3 < close3 and open3 < open1 and close1 < close3

def isOneWhiteSoldier(open1, close1, open2, close2):
    return open1 > close1 and open2 < close2 and close1 < open2 and open1 < close2 and open2 < open1

def isBullishEngulfing(open1, close1, open2, close2):
    return open1 > close1 and open2 < close2 and open2 <= close1 and open1 <= close2

# 84% bullish reversal
def isBearishThreeLineStrike(open1, close1, open2, close2, open3, close3, open4, close4):
    red_red_red_green = open1 > close1 and open2 > close2 and open3 > close3 and open4 < close4
    ratio_1_2 = close1 <= open2 and open2 < open1
    ratio_2_3 = close2 <= open3 and open3 < open2
    ratio_3_4 = open4 <= close3 and close4 >= open1
    return red_red_red_green and ratio_1_2 and ratio_2_3 and ratio_3_4

def isInRange1(value, low1, high1):
    return value >= low1 and value <= high1

def isInRange2(value, low1, high1, low2, high2):
    return (value > low1 or value > low2) and (value < high1 or value < high2)

def isInRange3(value, low1, high1, low2, high2, low3, high3):
    return (value > low1 or value > low2 or value > low3) and (value < high1 or value < high2 or value < high3)

def processSymbol(symbol, data, date_from, date_to):
    recent_signal = False  # if it has a signal in the last day(s)

    fig, ax = plt.subplots()

    opens = data['open']
    highs = data['high']
    lows = data['low']
    closes = data['close']

    mva_20 = getMva(closes, 20)
    ax.plot(mva_20[0], mva_20[1], color='b')

    mva_50 = getMva(closes, 50)
    ax.plot(mva_50[0], mva_50[1], color='y')

    mva_200 = getMva(closes, 200)
    ax.plot(mva_200[0], mva_200[1], color='g')

    length = len(opens)
    for i in range(length-2):
        open1 = opens[i]
        low1 = lows[i]
        close1 = closes[i]
        high1 = highs[i]
        open2 = opens[i+1]
        low2 = lows[i+1]
        close2 = closes[i+1]
        high2 = highs[i+1]
        open3 = 0
        low3 = 0
        close3 = 0
        high3 = 0
        open4 = 0
        low4 = 0
        close4 = 0
        high4 = 0
        if i <= length-3:
            open3 = opens[i+2]
            low3 = lows[i+2]
            close3 = closes[i+2]
            high3 = highs[i+2]
        if i <= length-4:
            open4 = opens[i+3]
            low4 = lows[i+3]
            close4 = closes[i+3]
            high4 = highs[i+3]

        # check candlestick aptterns
        morning_star = False
        bearish_three_line_strike = False
        if i <= length-3:
            morning_star = signals_check['morning_star'] and isMorningStar(open1, close1, open2, close2, open3, close3)
        if i <= length-4:
            bearish_three_line_strike = signals_check['bearish_three_line_strike'] and isBearishThreeLineStrike(open1, close1, open2, close2, open3, close3, open4, close4)
        one_white_soldier = signals_check['one_white_soldier'] and isOneWhiteSoldier(open2, close2, open3, close3)
        bullish_engulfing = signals_check['bullish_engulfing'] and isBullishEngulfing(open2, close2, open3, close3)

        is_signal = morning_star or bearish_three_line_strike or one_white_soldier or bullish_engulfing

        # check MVA's
        mva_bullish = False
        if i in mva_200[2]:
            mva_bullish = mva_20[2][i] > mva_50[2][i] and mva_50[2][i] > mva_200[2][i]

        if (not only_mva_bullish or mva_bullish) and is_signal:
            passes = False
            label = 'b'
            mva_50v = 0
            if only_mva_bullish:
                mva_50v = mva_50[2][i]
            if bearish_three_line_strike and (not only_touching_mva or isInRange1(mva_50v, low4, high4)):
                passes = True
                label = 'bearish three line strike'
                if i >= length - recent_signal_length:
                    recent_signal = True
            elif morning_star and (not only_touching_mva or isInRange3(mva_50v, low1, high1, low2, high2, low3, high3)):
                passes = True
                label = 'morning star'
                if i >= length - recent_signal_length:
                    recent_signal = True
            elif one_white_soldier and (not only_touching_mva or isInRange2(mva_50v, low2, high2, low3, high3)):
                passes = True
                label = 'one white soldier'
                if i >= length - recent_signal_length:
                    recent_signal = True
            elif bullish_engulfing and (not only_touching_mva or isInRange2(mva_50v, low2, high2, low3, high3)):
                passes = True
                label = 'bullish engulfing'
                if i >= length - recent_signal_length:
                    recent_signal = True
            if passes:
                plt.text(i, low1, label, rotation=270)

    if only_recent_signal and not recent_signal:
        pass  #  do nothing: it doesn't have a recent signal but it must have to be processed
    else:
        candlestick2_ohlc(ax, opens, highs, lows, closes, width=1, colorup='g', colordown='r')
        if save_figure:
            plt.savefig('{}/{}-{}.png'.format(charts_folder, date_to, symbol))
        if show_figure:
            plt.show()

    return recent_signal

symbols = ['TESS']
save_figure = False  # save chart figure to file
show_figure = True  # show chart figure with utility program to inspect it
only_recent_signal = False  # process only those that have a signal in the last day(s)
recent_signal_length = 10  # how many days we consider a recent signal
only_touching_mva = False  # passes only if the signal is in range of MVA value
only_mva_bullish = False  # passes only if MVA(20) > MVA(50) > MVA(200)
signals_check = {'bearish_three_line_strike': True, 'morning_star': False, 'one_white_soldier': False, 'bullish_engulfing': False}
charts_folder = 'charts'

# calculate from and to date
today = datetime.today()
date_to = today.strftime('%Y-%m-%d')
date_from = (today - timedelta(days=365)).strftime('%Y-%m-%d')

processed_tickers = []
recent_signal_tickers = []
batched_data = stockslib.getQuandlBatchedData(symbols, date_from, date_to)
for batch in batched_data:
    for ticker in batch:
        recent_signal = processSymbol(ticker, batch[ticker], date_from, date_to)
        processed_tickers.append(ticker)
        if recent_signal:
            recent_signal_tickers.append(ticker)

print('{} tickers processed: {}'.format(len(processed_tickers), processed_tickers))
print('{} recent signal tickers: {}'.format(len(recent_signal_tickers), recent_signal_tickers))
