This package is used to pull key people from a company based on the ticker.


from Key_People import get_Key_People, Key_People, get_c_Name
list_of_key_people = get_Key_People("AAPL")
company_Name = get_c_Name("AAPL")

#if you are doing multiple entries and want to make it quicker
db = Key_People()

entry = db.entry("AAPL")

entry.company_Name
entry.key_People
entry.ticker
