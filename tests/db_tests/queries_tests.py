from nose.tools import *
from db.queries import *

def test_cursor():
	c.execute("select name from tx where amount < 0")
	assert_equal(c.fetchone(), ("First withdrawal",) )

def test_create_transaction():
	create_transaction("2015-01-03", 200, "Visa payment", 20)
	c.execute("select name from tx where account = 200 and amount = 20")
	assert_equal(c.fetchone(), ("Visa payment", ))

def test_get_current_balance():
	assert_equal(get_current_balance(100), 1620)
	assert_equal(get_current_balance(100, '2015-01-01'), 1520)
	assert_equal(get_current_balance(100, '2015-01-03'), 1620)
	assert_equal(get_current_balance(100, '2014-06-03'), 20)
