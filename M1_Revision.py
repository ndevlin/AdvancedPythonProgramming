'''
Rotating Caesar Cypher encryption and decryption
Mid 1 Q
'''


class Decryption:

    def __init__(self, shift):
        self.shift = shift

    def caesarCypher(self, inputString):
        outputString = ""
        shift = self.shift
        for char in inputString:
            asciiVal = ord(char)
            newAsciiVal = asciiVal + shift
            if newAsciiVal > 0x80:
                newAsciiVal = newAsciiVal - 0x80 + 0x20 - 1
            outputString += chr(newAsciiVal)
            shift += 1
        return outputString

    def decryptCaesarCypher(self, inputString):
        outputString = ""
        shift = self.shift
        for char in inputString:
            asciiVal = ord(char)
            newAsciiVal = asciiVal - shift
            if newAsciiVal < 0x20:
                newAsciiVal = newAsciiVal + 0x80 - 0x20 + 1
            outputString += chr(newAsciiVal)
            shift += 1
        return outputString


# Main

stringToEncrypt = "HELLO"

decrypter = Decryption(shift=5)

print("Encrypt", stringToEncrypt)
encryptedString = decrypter.caesarCypher(stringToEncrypt)
print(encryptedString)

print("Decrypt ", encryptedString)
decryptedString = decrypter.decryptCaesarCypher(encryptedString)
print(decryptedString)



import sqlite3
import unittest

class SqliteManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print(f"Disconnected from database: {self.db_name}")

    def queryBuilder(self, query_type, table_name, query_tuple=None):
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

    def executeQuery(self, query_string):
        try:
            self.cursor.execute(query_string)
            self.connection.commit()
            print(f"Executed query: {query_string}")
            if query_string.split()[0].upper() == "SELECT" or query_string.split()[0].upper() == "WHERE":
                return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


class TestDecryption(unittest.TestCase):

    def testEncryptionDecryption(self):

        databaseName = "Mid1.db"

        with SqliteManager(databaseName) as db:

            tableTupleData = "(Text1 TEXT, Text2 TEXT)"

            # CREATE TABLE
            createTableQuery = db.queryBuilder('CREATE TABLE', 'TextTable', tableTupleData)
            db.executeQuery(createTableQuery)

            textToInsert = ("Hello", "World")
            insertQuery = db.queryBuilder('INSERT', 'TextTable', textToInsert)
            db.executeQuery(insertQuery)

            print(f"{insertQuery = }")
            print()

            decrypter = Decryption(shift=3)
            originalString = insertQuery
            print(f"{originalString = }")
            encryptedString = decrypter.caesarCypher(originalString)
            print(f"{encryptedString = }")
            decryptedString = decrypter.decryptCaesarCypher(encryptedString)
            print(f"{decryptedString = }")
            self.assertEqual(originalString, decryptedString)
            print("originalString == decryptedString?" , originalString == decryptedString)


if __name__ == '__main__':
    unittest.main()
