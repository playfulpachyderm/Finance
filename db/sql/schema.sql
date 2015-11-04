DROP TABLE IF EXISTS account_codes;
DROP TABLE IF EXISTS tx;

PRAGMA foreign_keys = ON;

CREATE TABLE account_codes (code integer primary key NOT NULL, name text);

CREATE TABLE tx (
	rowid integer primary key AUTOINCREMENT, -- builtin rowid doesn't allow foreign keys
	date date, account integer NOT NULL, name text, amount real NOT NULL, antitransaction integer,
	FOREIGN KEY(account) REFERENCES account_codes(code),
	FOREIGN KEY(antitransaction) REFERENCES tx(rowid)
);
