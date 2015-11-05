INSERT INTO "account_codes" VALUES(100, "BANK ACCOUNT 1"); -- Read only (see below)
INSERT INTO "account_codes" VALUES(110, "BANK ACCOUNT 2"); -- sandbox
INSERT INTO "account_codes" VALUES(200, "VISA");
INSERT INTO "account_codes" VALUES(400, "Salary (potato peeling)");
INSERT INTO "account_codes" VALUES(500, "EXPENSE ACCT 1");



/* 	Account 100 is assumed by tests to be unmodified other than here.	*
*	Writing tests which modify it may (non-deterministically) cause		*
*	other tests to break. 												*/

INSERT INTO "tx" VALUES(NULL, '2015-01-01',100,'First deposit',500.0, NULL);
INSERT INTO "tx" VALUES(NULL, '2015-01-01',100,'Second deposit',1000.0, NULL);
INSERT INTO "tx" VALUES(NULL, '2015-01-02',100,'First withdrawal',-200.0, NULL);
INSERT INTO "tx" VALUES(NULL, '2015-01-02',100,'Third deposit',300.0, NULL);
INSERT INTO "tx" VALUES(NULL, '2014-01-02',100,'Historical deposit!',20.0, NULL);

