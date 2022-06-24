import sqlite3
import json

class LocalBd:
    def createMySqlConnection(self):
        try:
            sqlite_connection = sqlite3.connect('sqlite_python.db')
            cursor = sqlite_connection.cursor()
            print("База данных создана и успешно подключена к SQLite")

            sqlite_select_query = "select sqlite_version();"
            cursor.execute(sqlite_select_query)
            record = cursor.fetchall()
            print("Версия базы данных SQLite: ", record)

        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)

        return sqlite_connection


    def CreateCursorFromConnection(self,connection):
        try:
            cursor = connection.cursor()
            return cursor
        except sqlite3 as ex:
            print(ex)

    def createNewTable(self,connection):
        cursor = self.CreateCursorFromConnection(connection)
        cursor.execute('''CREATE TABLE sorted_media_with_tags(mediaUrl TEXT NOT NULL, mediaType TEXT NOT NULL, Tags TEXT NOT NULL)''')



    def checkSqlVersion(self,connection):
        cursor = self.CreateCursorFromConnection(connection)
        sqlite_select_query = "select sqlite_version();"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        print("Версия базы данных SQLite: ", record)




Worker = LocalBd()
connection = Worker.createMySqlConnection()