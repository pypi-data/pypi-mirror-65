from database_Management import open_Connection, find_Ticker

class Key_People:
	def __init__(self):
		self.conn, self.c = open_Connection("DB/Stocks.db")

	def entry(self, ticker):
		ticker = ticker.upper()
		ticker = (ticker, )
		results = find_Ticker(ticker, self.c)[0]
		ticker = results[0]
		company_Name = results[1]
		people = []
		for x in results[2:]:
			if x != 'NULL':
				people.append(x)
		return entry(ticker, company_Name, people)

class entry:
	def __init__(self, ticker, company_Name, people):
		self.key_People = people
		self.company_Name = company_Name
		self.ticker = ticker

def get_Key_People(ticker):
	ticker = ticker.upper()
	conn, c = open_Connection("DB/Stocks.db")
	ticker = (ticker, )
	try:
		results = find_Ticker(ticker, c)[0]
		ticker = results[0]
		company_Name = results[1]
		people = []
		for x in results[2:]:
			if x != 'NULL':
				people.append(x)
		conn.close()
		return people
	except:
		raise Exception("Company not found (reminder: search by ticker)")

def get_c_Name(ticker):
	ticker = ticker.upper()
	conn, c = open_Connection("DB/Stocks.db")
	ticker = (ticker, )
	try:
		results = find_Ticker(ticker, c)[0]
		ticker = results[0]
		company_Name = results[1]
		conn.close()
		return company_Name
	except:
		raise Exception("Company not found (reminder: search by ticker)")

