import sqlite3

conn = sqlite3.connect('stocks.db')

c = conn.cursor()

c.execute("INSERT INTO stocks VALUES ('AAPL', '2018-01-01', 1, 2, 3, 4)")

conn.commit()

conn.close()
