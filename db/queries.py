import os
import sqlite3
from utils.date_utils import date_or_today

ASSETS = "Assets"
CURRENT_ASSETS = "Current assets"
LONG_TERM_ASSETS = "Long term assets"

LIABILITIES = "Liabilities"
CURRENT_LIABILITIES = "Current liabilities"
LONG_TERM_LIABILITIES = "Long term liabilities"

REVENUE = "Revenue"

EXPENSES = "%Expenses%"
LEGIT_EXPENSES = "Legitimate expenses"
OPT_EXPENSES = "Optional expenses"
RETARDED_EXPENSES = "Retarded expenses"
MISC_EXPENSES = "Misc expenses"

env = os.environ.setdefault("env_type", "prod")

db = {"prod": "finances.db", "test": ":memory:"}[env]
con = sqlite3.connect(db)
c = con.cursor()

def is_account_type(account, *types):
	q = """
		select *
		  from account_codes acct
		  join account_metacodes meta
		    on acct.code like meta.code
		 where ? like meta.code
		   and (
		        meta.type like ?
	  """ + "or meta.type like ?" * (len(types) - 1) + ")"
	c.execute(q, (account, ) + types)
	return bool(c.fetchone())


def create_transaction(date, account, name, amount, antitransaction = None):
	q = """insert into tx (date, account, name, amount, antitransaction) \
	               values (?, ?, ?, ?, ?)
	"""
	c.execute(q, (date, account, name, amount, antitransaction))

	# return new row's rowid
	c.execute("select last_insert_rowid() from tx")
	return c.fetchone()[0]

def create_transaction_with_mirror(date, account1, account2, name, amount):
	acct_type1 = is_account_type(account1, EXPENSES, LIABILITIES)
	acct_type2 = is_account_type(account2, EXPENSES, LIABILITIES)

	rowid1 = create_transaction(date, account1, name, amount)

	if acct_type1 != acct_type2:
		amount *= -1

	rowid2 = create_transaction(date, account2, name, amount, rowid1)
	c.execute("update tx set antitransaction = ? where rowid = ?", (rowid2, rowid1, ))
	return rowid1, rowid2

def get_current_balance(account, d = None):
	# returns the balance in the specified account at the end of the specified day
	# (defaults to today if no date is specified)

	q = """
	    select round(sum(t2.amount), 2)
	      from tx t1
	 left join tx t2
	        on (t1.date > t2.date or (t1.date = t2.date and t1.rowid >= t2.rowid))
	       and t1.account = t2.account
	     where t1.account = ?
	       and t1.date <= ?
	  group by t1.rowid
	  order by t1.date desc,
	           t1.rowid desc
	"""

	d = date_or_today(d)

	c.execute(q, (account, d))
	result = c.fetchone()
	if result != None:
		return result[0]
	else:
		return 0
