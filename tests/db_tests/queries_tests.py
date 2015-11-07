from nose.tools import *
from db.queries import *

def test_cursor():
	c.execute("select name from tx where amount < 0")
	assert_equal(c.fetchone(), ("First withdrawal",) )

def test_create_transaction():
	rowid = create_transaction("2015-01-03", 200, "Visa payment", 20)
	c.execute("select name from tx where rowid = ?", (rowid, ))
	assert_equal(c.fetchone(), ("Visa payment", ))

def test_is_account_type():
	assert_true(is_account_type(110, ASSETS))
	assert_true(is_account_type(110, LONG_TERM_ASSETS))
	assert_false(is_account_type(110, CURRENT_ASSETS))
	assert_false(is_account_type(110, LIABILITIES))

	assert_true(is_account_type(500, EXPENSES))
	assert_true(is_account_type(500, LEGIT_EXPENSES))
	assert_false(is_account_type(500, MISC_EXPENSES))


def test_create_transaction_with_mirror_correctly_creates_antitransactions():
	rowid1, rowid2 = create_transaction_with_mirror("2015-02-01", 110, 500, "Paying expense 1", -40)
	c.execute("select name, amount, antitransaction from tx where rowid = ?", (rowid1, ))
	assert_equal(c.fetchone(), ("Paying expense 1", -40, rowid2, ))
	c.execute("select name, amount, antitransaction from tx where rowid = ?", (rowid2, ))
	assert_equal(c.fetchone(), ("Paying expense 1", 40, rowid1, ))

	# Test all permutations
	rowid1, rowid2 = create_transaction_with_mirror("2015-02-01", 110, 400, "Two hours of potato peeling", 38)
	c.execute("select amount from tx where rowid = ?", (rowid2, ))
	assert_equal(c.fetchone(), (38, ))

	rowid1, rowid2 = create_transaction_with_mirror("2015-02-01", 200, 500, "paying with Visa", 38)
	c.execute("select amount from tx where rowid = ?", (rowid2, ))
	assert_equal(c.fetchone(), (38, ))

	rowid1, rowid2 = create_transaction_with_mirror("2015-02-01", 110, 200, "Two hours of potato peeling", 38)
	c.execute("select amount from tx where rowid = ?", (rowid2, ))
	assert_equal(c.fetchone(), (-38, ))

def test_get_current_balance():
	assert_equal(get_current_balance(100), 1620)
	assert_equal(get_current_balance(100, '2015-01-01'), 1520)
	assert_equal(get_current_balance(100, '2015-01-03'), 1620)
	assert_equal(get_current_balance(100, '2014-06-03'), 20)

def test_list_accounts():
	l = list_accounts(ASSETS)
	assert_in((100, "BANK ACCOUNT 1"), l)
	assert_in((110, "BANK ACCOUNT 2"), l)

	l = list_accounts(CURRENT_ASSETS)
	assert_in((100, "BANK ACCOUNT 1"), l)
	assert_not_in((110, "BANK ACCOUNT 2"), l)

	l = list_accounts(MISC_EXPENSES)
	assert_in((800, "lol"), l)
	assert_in((801, "lmao"), l)
