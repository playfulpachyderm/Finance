from db.queries import *
from utils.date_utils import date_or_today, output_format


# TODO: some of these should probably be broken into smaller methods.  They
# are way too huge, pretty WET, and generally clunky.
# The testing of these methods are shoddy at best for those reasons.


class document(object):
	def __init__(self, name, date = None, fill_char = " ", column_width = 9):
		self.name = name
		self.date = date_or_today(date)
		self.fill_char = fill_char
		self.column_width = column_width

	def format_line(self, acct_name, acct_balance, bonus_indent, dollar_sign = False):
		return "{:{fill_char}<50}{: <{margin}}{: >{column_width}.2f}".format(
			acct_name,
			"$" if dollar_sign else "",
			acct_balance,
			fill_char = self.fill_char,
			margin = 1 + bonus_indent * self.column_width,
			column_width = self.column_width
		)

	def format_block(self, block_name, acct_list, bonus_indent):
		s = "{}\n".format(block_name)
		total = 0

		for i, (acct_num, acct_name) in enumerate(acct_list):
			acct_balance = get_current_balance(acct_num, self.date)
			s += "{}\n".format(self.format_line(
				acct_name,
				acct_balance,
				bonus_indent,
				i == 0
			))
			total += acct_balance

		s += "{}\n\n".format(self.format_line(
			"Total " + block_name.lower(),
			total,
			bonus_indent + 1
		))

		return s, total


class balance_sheet(document):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def render(self):
		cur_asset_accts = list_accounts(CURRENT_ASSETS)
		cur_liab_accts 	= list_accounts(CURRENT_LIABILITIES)

		long_asset_accts = list_accounts(LONG_TERM_ASSETS)
		long_liab_accts = list_accounts(LONG_TERM_LIABILITIES)

		sheet = "{}\nBalance sheet\n{}\n\n".format(self.name, output_format(self.date))

		total_assets = 0
		sheet += "{}\n\n".format(ASSETS)
		block, cur_assets_amount = self.format_block(CURRENT_ASSETS, cur_asset_accts, 0)
		sheet += block
		total_assets += cur_assets_amount

		block, long_assets_amount = self.format_block(LONG_TERM_ASSETS, long_asset_accts, 0)
		sheet += block
		total_assets += long_assets_amount

		sheet += self.format_line("Total {}".format(ASSETS.lower()), total_assets, 2)

		sheet += "\n\n"

		total_liabs = 0
		sheet += "{}\n\n".format(LIABILITIES)
		block, cur_liabs_amount = self.format_block(CURRENT_LIABILITIES, cur_liab_accts, 0)
		sheet += block
		total_liabs += cur_liabs_amount

		block, long_liabs_amount = self.format_block(LONG_TERM_LIABILITIES, long_liab_accts, 0)
		sheet += block
		total_liabs += long_liabs_amount

		sheet += self.format_line("Total {}".format(LIABILITIES.lower()), total_liabs, 2) + "\n\n"

		sheet += self.format_line("Net worth", total_assets - total_liabs, 2)
		return sheet


class income_statement(document):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
