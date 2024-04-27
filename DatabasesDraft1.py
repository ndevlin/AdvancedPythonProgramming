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

    def query_builder(self, query_type, table_name, query_tuple=None):
        if query_type.upper() == "CREATE TABLE":
            query_string = f"CREATE TABLE IF NOT EXISTS {table_name} {query_tuple}"
        elif query_type.upper() == "INSERT":
            query_string = f"INSERT INTO {table_name} VALUES {query_tuple}"
        elif query_type.upper() == "SELECT":
            query_string = f"SELECT * FROM {table_name}"
        elif query_type.upper() == "WHERE":
            query_string = f"SELECT * FROM {table_name} WHERE {query_tuple}"
        elif query_type.upper() == "UPDATE":
            query_string = f"UPDATE {table_name} SET {query_tuple}"
        elif query_type.upper() == "DELETE":
            query_string = f"DELETE FROM {table_name} WHERE {query_tuple}"
        else:
            raise ValueError(f"Unsupported query type: {query_type}")
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

    # Create a table
    c.execute('''
        CREATE TABLE IF NOT EXISTS my_table (
            id TEXT,
            name TEXT,
            photo TEXT,
            html TEXT
        )
    ''')

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

print("Creating sample database...")
create_sample_database()

with SqliteManager('my_database.db') as db:
    # Test CREATE TABLE
    create_table_query = db.query_builder('CREATE TABLE', 'new_table', '(id INTEGER, name TEXT)')
    db.execute_query(create_table_query)

    # Test INSERT
    insert_query = db.query_builder('INSERT', 'my_table', "('my_id', 'my_name', 'my_photo', 'my_html')")
    db.execute_query(insert_query)

    # Test SELECT
    select_query = db.query_builder('SELECT', 'my_table')
    db.execute_query(select_query)

    # Test WHERE
    where_query = db.query_builder('WHERE', 'my_table', "id='my_id'")
    db.execute_query(where_query)

    # Test UPDATE
    update_query = db.query_builder('UPDATE', 'my_table', "name='new_name' WHERE id='my_id'")
    db.execute_query(update_query)

    # Test DELETE
    delete_query = db.query_builder('DELETE', 'my_table', "id='my_id'")
    db.execute_query(delete_query)