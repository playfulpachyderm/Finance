import sys
from db import import_transactions
from . import generate


# TODO: this should be a __doc__ somewhere
help_string = """\
This is Finance.  You can either import transactions to reset the db, or generate some documents.
To import transactions, add the arg "import".
To generate documents, add "generate balance_sheet" or something like that.
Exiting.
"""


if len(sys.argv) < 2:
	print(help_string)
	sys.exit(0)

# Obviously, change this line if this isn't your name
my_name = "Alessio Magnus"

def balance_sheet():
	print("Creating a balance sheet.")
	date = input("Enter date at which to create the balance sheet:\n> ").strip()
	bs = generate.balance_sheet(my_name, date)
	print(bs.render())



if sys.argv[1] == "import":
	import_transactions.main()
elif sys.argv[1] == "generate":
	if sys.argv[2] == "balance_sheet":
		balance_sheet()
	elif sys.argv[2] == "income_statement":
		income_statement()
