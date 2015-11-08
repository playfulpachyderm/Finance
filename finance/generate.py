from db.queries import *
from utils.date_utils import date_or_today, output_format


# TODO: some of these should probably be broken into smaller methods.  They
# are way too huge, pretty WET, and generally clunky.
# The testing of these methods are shoddy at best for those reasons.


class document(object):
	def __init__(self, name, date = None, from_date = None, fill_char = " ", column_width = 9):
		self.name = name
		self.date = date_or_today(date)
		self.from_date = from_date or "0001-01-01"
		self.fill_char = fill_char
		self.column_width = column_width

	def format_line(self, acct_name, acct_balance, bonus_indent, dollar_sign = False):
		if not acct_balance:
			return ""

		else:
			return "{:{fill_char}<50}{: <{margin}}{: >{column_width}.2f}\n".format(
				acct_name,
				"$" if dollar_sign else "",
				acct_balance,
				fill_char = self.fill_char,
				margin = 1 + bonus_indent * self.column_width,
				column_width = self.column_width
			)

class balance_sheet(document):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def format_block(self, block_name, block, bonus_indent):

		s = "{}\n".format(block_name)
		total = 0

		for i, (acct_num, acct_name) in enumerate(block):
			acct_balance = get_current_balance(acct_num, self.date)
			s += "{}".format(self.format_line(
				acct_name,
				acct_balance,
				bonus_indent,
				i == 0
			))
			total += acct_balance

		s += "{}\n".format(self.format_line(
			"Total " + block_name.lower(),
			total,
			bonus_indent + 1
		))

		return s, total

	def render(self):
		# Note: this method has no tests!!!!

		sheet = "{}\nBalance sheet\n{}\n\n".format(self.name, output_format(self.date))

		total_assets = 0
		sheet += "{}\n\n".format(ASSETS)
		block, cur_assets_amount = self.format_block(CURRENT_ASSETS, list_accounts(CURRENT_ASSETS), 0)
		sheet += block
		total_assets += cur_assets_amount

		block, long_assets_amount = self.format_block(LONG_TERM_ASSETS, list_accounts(LONG_TERM_ASSETS), 0)
		sheet += block
		total_assets += long_assets_amount

		sheet += self.format_line("Total {}".format(ASSETS.lower()), total_assets, 2)

		sheet += "\n"

		total_liabs = 0
		sheet += "{}\n".format(LIABILITIES)
		block, cur_liabs_amount = self.format_block(CURRENT_LIABILITIES, list_accounts(CURRENT_LIABILITIES), 0)
		sheet += block
		total_liabs += cur_liabs_amount

		block, long_liabs_amount = self.format_block(LONG_TERM_LIABILITIES, list_accounts(LONG_TERM_LIABILITIES), 0)
		sheet += block
		total_liabs += long_liabs_amount

		sheet += self.format_line("Total {}".format(LIABILITIES.lower()), total_liabs, 2) + "\n"

		sheet += self.format_line("Net worth", total_assets - total_liabs, 2)
		return sheet


class income_statement(document):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def format_block(self, block_name, block, bonus_indent):

		s = "{}\n".format(block_name)
		total = 0

		for i, (acct_num, acct_name) in enumerate(block):
			acct_balance = get_balance_change(acct_num, self.from_date, self.date)
			s += "{}".format(self.format_line(
				acct_name,
				acct_balance,
				bonus_indent,
				i == 0
			))
			total += acct_balance

		s += "{}\n".format(self.format_line(
			"Total " + block_name.lower(),
			total,
			bonus_indent + 1
		))

		return s, total

	def render(self):
		# Note: this method has no tests!!!!

		sheet = "{}\nIncome Statement\n{}\n\n".format(
			self.name,
			output_format(self.from_date) + " to " + output_format(self.date)
		)

		sheet += "{}\n\n".format(REVENUE)
		block, total_rev = self.format_block(REVENUE, list_accounts(REVENUE), 1)
		sheet += block

		sheet += "\n"

		total_exp = 0
		sheet += "{}\n\n".format(EXPENSES.strip("%"))

		for exp in [LEGIT_EXPENSES, OPT_EXPENSES, RETARDED_EXPENSES, MISC_EXPENSES]:
			block, amount = self.format_block(exp, list_accounts(exp), 0)
			sheet += block
			total_exp += amount

		sheet += self.format_line("Total {}".format(EXPENSES.strip("%").lower()), total_exp, 2) + "\n\n"

		sheet += self.format_line("Net income", total_rev - total_exp, 2)
		return sheet
