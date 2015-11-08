from sqlite3 import IntegrityError
from nose.tools import *
from db.queries import c

# ********** account_codes tests *********

def test_account_codes_insert_trigger_rejects_nonmeta_codes():
	q = "insert into account_codes (code, name) values (1, \"an invalid account\")"
	assert_raises(IntegrityError, c.execute, q)

def test_account_codes_rejects_duplicate_code():
	q = "insert into account_codes (code, name) values (100, \"a duplicate account\")"
	assert_raises(IntegrityError, c.execute, q)

def test_create_valid_account_code():
	q1 = "insert into account_codes (code, name) values (101, \"a valid account\")"
	q2 = "select * from account_codes where code = 101"
	c.execute(q1)
	c.execute(q2)
	assert_equal(c.fetchone(), (101, "a valid account"))

# *************** tx tests ****************

def test_create_tx_with_invalid_or_null_account_code_fails():
	q = "insert into tx (date, account, name, amount) values ('2015-01-01', -1, 'accountless tx', 100)"
	assert_raises(IntegrityError, c.execute, q)

	q = "insert into tx (date, account, name, amount) values ('2015-01-01', NULL, 'accountless tx', 100)"
	assert_raises(IntegrityError, c.execute, q)

def test_create_tx_with_null_amount_fails():
	q = "insert into tx (date, account, name, amount) values ('2015-01-01', 100, 'null tx', NULL)"
	assert_raises(IntegrityError, c.execute, q)

def test_invalid_antitransaction_fails():
	q = "insert into tx(account, amount, antitransaction) values(100, 100, -1)"
	assert_raises(IntegrityError, c.execute, q)

def test_create_valid_tx():
	q1 = "insert into tx (date, account, name, amount, antitransaction) \
				  values ('2015-01-01', 110, 'valid tx', 100, 1)"
	q2 = "select name from tx where account = 110 and amount = 100"
	c.execute(q1)
	c.execute(q2)
	assert_equal(c.fetchone(), ("valid tx", ))

def test_tx_autoincrement():
	# This is kind of a weak test, maybe get rid of it?
	q1 = "select max(rowid) from tx"
	q2 = "insert into tx (account, amount) values (100, 100)"
	q3 = "select last_insert_rowid() from tx"

	max_rowid = c.execute(q1).fetchone()[0]
	c.execute(q2)
	c.execute(q3)
	assert_greater(c.fetchone()[0], max_rowid)
