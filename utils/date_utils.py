from datetime import date
from time import strftime, strptime

def output_format(d):
	return strftime("%B %d, %Y", strptime(d, "%Y-%m-%d"))

def date_or_today(d):
	# make d default to today
	return d or date.today().strftime("%Y-%m-%d")
