import sys
try:
	from db import import_transactions
except ImportError:
	pass
from . import generate


# TODO: this should be a __doc__ somewhere
help_string = """\
This is Finance.  You can either import transactions to reset the db, or
generate some documents.
To import transactions, add the arg "import".
To generate documents, add "generate balance_sheet" or something like that.
Exiting.
"""

no_import_transactions = """\
To use the "import" command, you have to create a file: "db/import_transactions.py"
and define a "main" method inside it.  See error info below.  More details can
be found in the README.md file.
"""


if len(sys.argv) < 2:
	print(help_string)
	sys.exit(0)

# Obviously, change this line if this isn't your name
my_name = "Alessio Magnus"

def balance_sheet():
	print("Creating a balance sheet.")
	date = input("Enter date at which to create the balance sheet:\n> ").strip()
	doc = generate.balance_sheet(my_name, date = date)
	print(doc.render())

def income_statement():
	print("Creating an income statement.")
	date = input("Enter start date:\n> ").strip()
	date2 = input("Enter end date:\n> ").strip()
	doc = generate.income_statement(my_name, from_date = date, date = date2)
	print(doc.render())

if sys.argv[1] == "import":
	try:
		# force a NameError
		# this avoids catching NameErrors inside the method
		a = import_transactions.main
	except NameError:
		print(no_import_transactions)
		raise

	a()

elif sys.argv[1] == "generate":
	if sys.argv[2] == "balance_sheet":
		balance_sheet()
	elif sys.argv[2] == "income_statement":
		income_statement()
