import sqlite3
import json
import pymysql
from psycopg import sql



class LocalBd:
    host = "127.0.0.1"
    user = "Popa"
    password = "200218kirill"
    db_name = "smartinv"
    BdTags = ["ВремяСуток", "ВремяГода", "Местность", "Авиа", "Автомобили", "БПЛА", "Водолаз", "Кинолог", "Кони", "Обьятия", "Шерп"]

    def createMySqlConnection(self,host = "127.0.0.1",user = "Popa",password = "200218kirill",db_name = "smartinv"):
        try:
            connection = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Соединение установлено")
            return connection

        except Exception as ex:
            print("Jopa")
            print(ex)


    def CreateCursorFromConnection(self,connection):
        try:
            cursor = connection.cursor()
            return cursor
        except sqlite3 as ex:
            print(ex)


    def createNewTable(self):
        connection = self.createMySqlConnection()
        cursor = self.CreateCursorFromConnection(connection)
        cursor.execute('''CREATE TABLE sorted_media_with_tags(mediaUrl VARCHAR(500) NOT NULL PRIMARY KEY, Tags TEXT, FULLTEXT KEY findTag (Tags))''')
        cursor.close()
        self.closeConnection(connection)


    def closeConnection(self, connection):
        connection.close()
        print("Соединенее закрыто")


    def selectRows(self):
        connection = self.createMySqlConnection()
        cursor = self.CreateCursorFromConnection(connection)
        cursor.execute('''SELECT * FROM `sorted_media_with_tags`''')
        record = cursor.fetchall()
        self.closeConnection(connection)
        return record


    def dropTable(self):
        connection = self.createMySqlConnection()
        cursor = self.CreateCursorFromConnection(connection)
        cursor.execute('''DROP TABLE `sorted_media_with_tags`''')
        self.closeConnection(connection)


    def findImageNameByTag(self,findTag):
        connection = self.createMySqlConnection()
        cursor = self.CreateCursorFromConnection(connection)
        cursor.execute('''SELECT mediaUrl FROM sorted_media_with_tags where match (Tags) AGAINST("%s")''',findTag)
        images = cursor.fetchall()
        self.closeConnection(connection)
        return images


    def findImagesNameByTwoTag(self, findTag, findTag2):
        connection = self.createMySqlConnection()
        cursor = self.CreateCursorFromConnection(connection)
        cursor.execute('''SELECT mediaUrl FROM sorted_media_with_tags where match (Tags) AGAINST ("+%s*+%s*")''',(findTag,findTag2))
        images = cursor.fetchall()
        self.closeConnection(connection)
        return images

    def findImagesNameByThreeTag(self, findTag, findTag2, findTag3):
        connection = self.createMySqlConnection()
        cursor = self.CreateCursorFromConnection(connection)
        cursor.execute('''SELECT mediaUrl FROM sorted_media_with_tags where match (Tags) AGAINST ("+%s*+%s*+%s*")''',(findTag,findTag2,findTag3))
        images = cursor.fetchall()
        self.closeConnection(connection)
        return images


    def getTagsByMediaName(self,mediaName):
        connection = self.createMySqlConnection()
        cursor = self.CreateCursorFromConnection(connection)
        cursor.execute('''SELECT Tags FROM `sorted_media_with_tags` WHERE mediaUrl = %s''',mediaName)
        Tags = cursor.fetchone()
        self.closeConnection(connection)
        return Tags


    def addNewTagToTagsOfMedia(self,tag,mediaName):
        connection = self.createMySqlConnection()
        cursor = self.CreateCursorFromConnection(connection)
        tagsDict = self.getTagsByMediaName(mediaName)
        print(tagsDict)
        appendedDict = self.appendTagToList(tag, tagsDict)
        print(appendedDict)
        self.pasteTagsByMediaName(appendedDict,mediaName)



    def appendTagToList(self, tag, tagsDict = {}):
        tagsDict["Tags"].append(tag)
        return tagsDict


    def pasteTagsByMediaName(self,tags,mediaName):
        connection = self.createMySqlConnection()
        cursor = self.CreateCursorFromConnection(connection)
        cursor.execute("UPDATE sorted_media_with_tags SET Tags = %s WHERE mediaUrl = %s",(tags,mediaName))
        connection.commit()
        self.closeConnection(connection)


    def addNewMediaAndTag(self,mediaName,Tags):
        connection = self.createMySqlConnection()
        cursor = self.CreateCursorFromConnection(connection)
        cursor.execute("INSERT INTO sorted_media_with_tags (mediaUrl,Tags) VALUES (%s,%s)", (mediaName, Tags))
        connection.commit()
        self.closeConnection(connection)




Worker = LocalBd()
work = Worker.getTagsByMediaName('Аываывац')
print(work)
Worker.addNewTagToTagsOfMedia('киса','Аываывац')
#Worker.dropTable()
#Worker.createNewTable()



