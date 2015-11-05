DROP TABLE IF EXISTS account_metacodes;
DROP TABLE IF EXISTS account_codes;
DROP TABLE IF EXISTS tx;

PRAGMA foreign_keys = ON;

CREATE TABLE account_metacodes(code text, type text);
/*************************************************************************
*************************** CHART OF ACCOUNTS ****************************
*
* 	Use this template when filling in the account_codes table.
*
*************************************************************************/

INSERT INTO "account_metacodes" VALUES('1__', 'ASSETS');
INSERT INTO "account_metacodes" VALUES('10_', 'CURRENT ASSETS');
INSERT INTO "account_metacodes" VALUES('11_', 'LONG TERM ASSETS');

INSERT INTO "account_metacodes" VALUES('2__', 'LIABILITIES');
INSERT INTO "account_metacodes" VALUES('20_', 'CURRENT LIABILITIES');
INSERT INTO "account_metacodes" VALUES('21_', 'LONG TERM  LIABILITIES');

INSERT INTO "account_metacodes" VALUES('4__', 'REVENUE');

INSERT INTO "account_metacodes" VALUES('5__', 'LEGITIMATE EXPENSES');
INSERT INTO "account_metacodes" VALUES('6__', 'OPTIONAL EXPENSES');
INSERT INTO "account_metacodes" VALUES('7__', 'RETARDED EXPENSES');
INSERT INTO "account_metacodes" VALUES('8__', 'MISC EXPENSES');


CREATE TABLE account_codes (code integer primary key NOT NULL, name text);

-- A pseudo foreign key, but compares using 'like' instead of '='
CREATE TRIGGER account_codes_insert BEFORE INSERT ON account_codes
BEGIN
	SELECT raise(ABORT, "Invalid code: must match at least 1 metacode from 'account_metacodes'")
	 where (SELECT type FROM account_metacodes WHERE new.code like account_metacodes.code) is NULL;
END;


CREATE TABLE tx (
	rowid integer primary key AUTOINCREMENT, -- builtin rowid doesn't allow foreign keys
	date date, account integer NOT NULL, name text, amount real NOT NULL, antitransaction integer,
	FOREIGN KEY(account) REFERENCES account_codes(code),
	FOREIGN KEY(antitransaction) REFERENCES tx(rowid)
);
