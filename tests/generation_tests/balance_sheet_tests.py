from nose.tools import *
from finance.generate import *

# Note: these tests suck.  Do not depend on them, they don't really
# assure a reasonable degree of integrity.
# This is probably a problem with how the balance sheet rendering is
# implemented (see the file for more info).

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
