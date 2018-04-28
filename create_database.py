import sqlite3

conn = sqlite3.connect('stocks.db')

c = conn.cursor()

c.execute('DROP TABLE IF EXISTS stocks')
conn.commit()

c.execute('''CREATE TABLE stocks
             (symbol text, date date, open real, high real, low real, close real, CONSTRAINT symbol_unique UNIQUE (symbol, date))''')
conn.commit()

conn.close()
