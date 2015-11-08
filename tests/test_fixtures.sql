INSERT INTO "account_codes" VALUES(100, "BANK ACCOUNT 1"); -- Read only (see below)
INSERT INTO "account_codes" VALUES(110, "BANK ACCOUNT 2"); -- sandbox
INSERT INTO "account_codes" VALUES(200, "VISA");
INSERT INTO "account_codes" VALUES(400, "Salary (potato peeling)");
INSERT INTO "account_codes" VALUES(500, "EXPENSE ACCT 1");


INSERT INTO "account_codes" VALUES(800, "lol");
INSERT INTO "account_codes" VALUES(801, "lmao");
INSERT INTO "account_codes" VALUES(802, "rofl");



/* 	The following accounts are assumed by tests to be unmodified other than		*
*	here.  Writing tests which modify them may (non-deterministically) cause	*
*	other tests to break. 														*/

INSERT INTO "tx" VALUES(NULL, '2015-01-01',100,'First deposit',500.0, NULL);
INSERT INTO "tx" VALUES(NULL, '2015-01-01',100,'Second deposit',1000.0, NULL);
INSERT INTO "tx" VALUES(NULL, '2015-01-02',100,'First withdrawal',-200.0, NULL);
INSERT INTO "tx" VALUES(NULL, '2015-01-02',100,'Third deposit',300.0, NULL);
INSERT INTO "tx" VALUES(NULL, '2014-06-02',100,'Historical deposit!',20.0, NULL);

INSERT INTO "tx" VALUES(NULL, '2014-01-01',100,'asdf',100, NULL);
INSERT INTO "tx" VALUES(NULL, '2014-02-02',100,'asdf',80, NULL);
INSERT INTO "tx" VALUES(NULL, '2014-02-03',100,'asdf',-100, NULL);
INSERT INTO "tx" VALUES(NULL, '2014-03-02',100,'asdf',100, NULL);

INSERT INTO "tx" VALUES(NULL, '2014-01-02',800,'some deposit',67.89, NULL);
INSERT INTO "tx" VALUES(NULL, '2014-01-02',801,'some deposit',123.45, NULL);
INSERT INTO "tx" VALUES(NULL, '2014-01-02',802,'some deposit',123234.45, NULL);
