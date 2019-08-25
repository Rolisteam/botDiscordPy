# -*- coding: utf-8 -*-
import mysql.connector
import json

class DataRetriver:

    def __init__(self, hostname, login, password, base):
        try:
            self.conn=mysql.connector.connect(host=hostname, user=login, passwd=password, database=base, charset='utf8mb4',use_unicode=True)
#            self.conn.autocommit(True)
            if self.conn.is_connected():
                print('Connected to Mysql database')
                self.mydb = self.conn.cursor()
        except Error as e:
            print(e)

    """Prefix"""
    def getPrefix(self, idx):
        sql = ("SELECT prefix FROM prefix WHERE id_server= %s ")
        self.mydb.execute(sql, (idx,))
        try:
            return self.mydb.fetchone()[0]
        except:
            return "!"

    def setPrefix(self, id, prefix):
        sql=""
        if( prefix == '!'):
            sql="DELETE FROM prefix where id_server=%s"
            self.mydb.execute(sql, (id,))
            self.conn.commit()
        else:
            try:
                print("insert into")
                sql="INSERT INTO prefix (id_server, prefix) VALUES (%s,%s);"
                self.mydb.execute(sql, (id, prefix))
                self.conn.commit()
                print(self.mydb.rowcount, "record inserted.")
            except:
                print("update prefix")
                sql="UPDATE prefix SET prefix = %s WHERE  id_server = %s"
                self.mydb.execute(sql, (prefix, id))
                self.conn.commit()

    """Macro"""
    def addMacro(self, id, pattern, cmd, regexp, comment):
        sql="INSERT INTO macro (id_server, pattern, cmd, regularexp, comment) VALUES(%s,%s,%s,%s,%s)"
        self.mydb.execute(sql, (id, pattern, cmd, regexp, comment))
        self.conn.commit()

    def removeMacro(self, id, index):
        sql = "select id from macro where id_server= %s"
        self.mydb.execute(sql, (id,))
        array = self.mydb.fetchall()
        sql = "DELETE FROM macro where id = %s"
        try:
            self.mydb.execute(sql, (array[index],))
            self.conn.commit()
        except Error as e:
            print(e)

    def showMacro(self, id, index):
        sql = "select * from macro where id_server= %s"
        self.mydb.execute(sql, (id,))
        data = self.mydb.fetchall()
        payload = []
        content = {}
        for result in data:
            content = {'pattern': result[1], 'cmd': result[2], 'regexp': result[3], 'comment': result[4]}
            payload.append(content)
            content = {}
        return json.dumps(payload)

    def getJsonMacro(self, id):
        sql = "select * from macro where id_server= %s"
        self.mydb.execute(sql, (id,))
        data = self.mydb.fetchall()
        payload = []
        content = {}
        for result in data:
            content = {'pattern': result[1], 'cmd': result[2], 'regexp': result[3], 'comment': result[4]}
            payload.append(content)
            content = {}
        return json.dumps(payload)




    """Alias"""
    def addAlias(self, id, pattern, cmds):
        sql="INSERT INTO alias (id_server, pattern, command) VALUES(%s,%s,%s)"
        self.mydb.execute(sql, (id,pattern , cmds))
        self.conn.commit()

    def removeAlias(self, id, index):
        sql = "SELECT id FROM alias WHERE id_server= %s"
        self.mydb.execute(sql, (id,))
        array = self.mydb.fetchAll()
        sql = "DELETE FROM alias where id = %s"
        try:
            self.mydb.execute(sql, (array[index],))
            self.conn.commit()
        except:
            pass


    def getAliases(self, id, pattern):
        sql = "SELECT command FROM alias WHERE id_server= %s AND pattern=%s"
        self.mydb.execute(sql, (id,pattern))
        try:
            data = self.mydb.fetchone()
            cmds=data[0]
            return cmds.split('\n')
        except:
            return None





    def showAlias(self, id, index):
        sql = "SELECT pattern,command FROM alias WHERE id_server= %s"
        self.mydb.execute(sql, (id,))
        data = self.mydb.fetchall()
        payload = []
        content = {}
        for result in data:
            content = {'pattern': result[0], 'cmds': result[1]}
            payload.append(content)
            content = {}
        return json.dumps(payload)
