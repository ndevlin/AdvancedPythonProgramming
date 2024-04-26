import sqlite3

class SqliteManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print(f"Disconnected from database: {self.db_name}")

    def query_builder(self, query_type, query_tuple):
        if query_type.upper() == "INSERT":
            query_string = f"INSERT INTO my_table VALUES {query_tuple}"
        elif query_type.upper() == "SELECT":
            query_string = f"SELECT * FROM my_table WHERE {query_tuple}"
        # Add more query types as needed
        else:
            raise ValueError(f"Unsupported query type: {query_type}")
        print(f"Built query: {query_string}")
        return query_string

    def execute_query(self, query_string):
        try:
            self.cursor.execute(query_string)
            self.conn.commit()
            print(f"Executed query: {query_string}")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

def create_sample_database():
    # Connect to the SQLite database
    # If the database does not exist, it will be created
    conn = sqlite3.connect('my_database.db')

    # Create a cursor object
    c = conn.cursor()

    # Drop the table if it already exists
    c.execute("DROP TABLE IF EXISTS my_table")
    print("Dropped table 'my_table' if it existed.")

    # Create a new table
    c.execute('''
        CREATE TABLE my_table (
            id TEXT,
            name TEXT,
            photo TEXT,
            html TEXT
        )
    ''')
    print("Created new table 'my_table'.")

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

print("Creating sample database...")
create_sample_database()

with SqliteManager('my_database.db') as db:
    query_tuple = ('my_id', 'my_name', 'my_photo', 'my_html')
    query_string = db.query_builder('INSERT', query_tuple)
    db.execute_query(query_string)

