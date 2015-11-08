# Finance

My personal accounting app, written in Python.

The purpose of this app is to keep track of all my financial transactions and categorize them.  It can then generate some documents to display this information.  A lot of this app was inspired by some high school accounting courses I took, and it attempts to apply some of the relevant accounting principles.

Some of the code is private, since I don't want to publish my banking information on Github.  Therefore the app can't quite be used "as is".  A brief explanation of what's missing is below.

Some of the app (see below for details) can be run from command line using the `-m` flag:
```
python -m finance [...]
```

## Accounts and storage

This app stores a record of all my financial transactions and purchases in a SQLite database `finances.db`.   Its schema can be found in `db/sql/schema.sql`.  This file defines a transaction table, an account table, and a set of account "metacodes" which acts as a sort of generic chart of accounts, using SQL wildcards to indicate a range of values.  If you want a different account structure, change these since the document generation depends on those values.

An important file is `db/sql/private/accounts.sql`, which contains a listing of the accounts.  (Note that this file is in the `.gitignore`, because it's private.) You have to set up your own list of accounts based on what you do with your money.  A (somewhat non-helpful) example of this in action are the accounts used by the tests, which can be found in `tests/test_fixtures.sql`.

The other hidden file is `db/import_transactions.py`.  This file can contain whatever you want; its only significance is that the following command will run `db.import_transaction.main()`, whatever you define that to be:
```
python -m finance import
```
The purpose of this is assumed to be to import a bunch of transactions into the `finances.db` database.  Where you want to import from and how you want to do this is up to you.

## Document generation

Documents are generated using:
```
python -m finance generate [balance_sheet | income_statement]
```
You can generate either a balance sheet or an income statement.  A balance sheet shows a snapshot of your total financial situation, whereas an income statement shows its change over a specified time period.

The prompts require dates to be given in the format `YYYY-MM-DD` since this is the format used by SQLite.

## Tests

This app is pretty well-tested.  It uses nosetests, so you can run them with:
```
nosetests
```

Nosetests uses automatic test detection, which basically means it looks inside the folder called `tests` and runs everything which is called `test` as a test.  For example, the `test_create_valid_tx` function inside `tests/db_tests/schema_tests.py`.  Check out the [doc page](https://nose.readthedocs.org/en/latest/) for more info.

Note: the document generation portion is currently not tested very well.
