from mpl_finance import candlestick2_ohlc
import matplotlib.pyplot as plt

quotes = {}

quotes['open'] = [1,2,3,4]
quotes['high'] = [2,3,4,4.5]
quotes['low'] = [0,1,2,3]
quotes['close'] = [1.5,2.5,3.5,3.5]

fig, ax = plt.subplots()
candlestick2_ohlc(ax,quotes['open'],quotes['high'],quotes['low'],quotes['close'],width=0.1)

plt.show()
