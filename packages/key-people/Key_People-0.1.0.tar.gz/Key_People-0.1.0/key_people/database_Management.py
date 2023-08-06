import sqlite3

def create_Table(c):
	c.execute('''CREATE TABLE stocks
             (symbol text, name text, key_person_1 text, key_person_2 text, key_person_3 text, key_person_4 text, key_person_5 text, key_person_6 text)''')

def find_Ticker(ticker, c):
	c.execute('SELECT * FROM stocks WHERE symbol=?', ticker)
	return c.fetchmany()

def add_Entry(entry, c):
	c.execute('INSERT INTO stocks VALUES (?,?,?,?,?,?,?,?)', entry)

def add_Many_Entry(entries, c):
	c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?,?,?,?)', entries)

def open_Connection(file):
	conn = sqlite3.connect(file)
	c = conn.cursor()
	return conn, c

def commit_Close(conn):
	conn.commit()
	conn.close()

