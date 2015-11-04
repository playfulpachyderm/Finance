import os
import sqlite3
from datetime import date

env = os.environ.setdefault("env_type", "prod")

db = {"prod": "finances.db", "test": ":memory:"}[env]
con = sqlite3.connect(db)
c = con.cursor()

def create_transaction(date, account, name, amount, antitransaction = None):
	c.execute("insert into tx (date, account, name, amount, antitransaction) \
				   values (?, ?, ?, ?, ?)",
						  (date, account, name, amount, antitransaction))

	# return new row's rowid
	c.execute("select last_insert_rowid() from tx")
	return c.fetchone()

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

	if not d:
		d = date.today().strftime("%Y-%m-%d")

	c.execute(q, (account, d))
	return c.fetchone()[0]
