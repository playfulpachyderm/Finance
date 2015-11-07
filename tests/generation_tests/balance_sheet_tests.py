import re
from nose.tools import *
from utils.date_utils import date_or_today
from finance.generate import *

# Note: these tests suck.  Do not depend on them, they don't really
# assure a reasonable degree of integrity.
# This is probably a problem with how the balance sheet rendering is
# implemented (see the file for more info).

def test_document_init():
	doc = document("Alessio", '2015-01-01', '.', 100)
	assert_equal(doc.name, "Alessio")
	assert_equal("2015-01-01", doc.date)
	assert_equal(doc.fill_char, ".")
	assert_equal(doc.column_width, 100)

def test_document_init_defaults():
	doc = document("Alessio")
	assert_equal(doc.name, "Alessio")
	assert_true(re.match("\d\d\d\d-\d\d-\d\d", doc.date))
	assert_equal(doc.fill_char, " ")
	assert_equal(doc.column_width, 9)

def test_format_line_works():
	doc = document("Alessio")
	assert_equal(doc.format_line("one acct", 57.893, 0, True),
		"""one acct                                          $    57.89""")

def test_format_line_rounds_to_nearest_cent():
	doc = document("Alessio")
	assert_equal(doc.format_line("two acct", 99.999, 0),
		"""two acct                                              100.00""")

def test_format_line_adds_extra_indenting():
	doc = document("Alessio", fill_char = "j")
	assert_equal(doc.format_line("one acct", 20, 1, True),
		"""one acctjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj$             20.00""")

def test_format_line_supports_variable_margin_widths():
	doc = document("Alessio", column_width = 3)
	assert_equal(doc.format_line("one acct", 20, 1, True),
		"""one acct                                          $   20.00""")

def test_format_block():
	bs = balance_sheet("Alessio")
	block, _ = bs.format_block(
		"Das Block",
		[(800, "lol"), (801, "lmao"), (802, "rofl")],
		0
	)
	das_block = \
"""\
Das Block
lol                                               $    67.89
lmao                                                  123.45
rofl                                               123234.45
Total das block                                             123425.79

"""

	assert_equal(block, das_block)
