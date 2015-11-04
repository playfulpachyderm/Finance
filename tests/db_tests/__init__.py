from db.queries import con

# Create test fixtures

def setup():
	schema = open("db/sql/schema.sql").read()
	fixtures = open("tests/test_fixtures.sql").read()

	con.executescript(schema)
	con.executescript(fixtures)
