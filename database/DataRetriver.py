# -*- coding: utf-8 -*-
import mysql.connector
import json

class DataRetriver:

    def __init__(self, hostname, login, password, base):
        try:
            self.conn=mysql.connector.connect(host=hostname, user=login, passwd=password, database=base, charset='utf8mb4',use_unicode=True)
            if self.conn.is_connected():
                print('Connected to Mysql database')
                self.mydb = self.conn.cursor()
        except Error as e:
            print(e)

    def connection(self):
        if not self.conn.is_connected():
            try:
                self.conn=mysql.connector.connect(host=hostname, user=login, passwd=password, database=base, charset='utf8mb4',use_unicode=True)
                if self.conn.is_connected():
                    print('Connected to Mysql database')
                    self.mydb = self.conn.cursor()
            except Error as e:
                print(e)

    """Prefix"""
    def getPrefix(self, idx):
        self.connection()
        sql = ("SELECT prefix FROM prefix WHERE id_server= %s ")
        self.mydb.execute(sql, (idx,))
        try:
            return self.mydb.fetchone()[0]
        except:
            return "!"

    def setPrefix(self, id, prefix):
        self.connection()
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
            except:
                print("update prefix")
                sql="UPDATE prefix SET prefix = %s WHERE  id_server = %s"
                self.mydb.execute(sql, (prefix, id))
                self.conn.commit()

    def lineAffected(self):
        return self.mydb.rowcount

    """Macro"""
    def addMacro(self, id, pattern, cmd, regexp, comment):
        self.connection()
        sql="INSERT INTO macro (id_server, pattern, cmd, regularexp, comment) VALUES(%s,%s,%s,%s,%s)"
        self.mydb.execute(sql, (id, pattern, cmd, regexp, comment))
        self.conn.commit()

    def removeMacro(self, id, index):
        self.connection()
        sql = "select id from macro where id_server= %s"
        self.mydb.execute(sql, (id,))
        array = self.mydb.fetchall()
        sql = "DELETE FROM macro where id = %s"
        try:
            self.mydb.execute(sql, (array[index][0],))
            self.conn.commit()
        except Exception as e:
            print("Invalid SQL: {}".format(e.message))

    def showMacro(self, id, index):
        self.connection()
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
        self.connection()
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
        self.connection()
        sql="INSERT INTO alias (id_server, pattern, command) VALUES(%s,%s,%s)"
        self.mydb.execute(sql, (id,pattern,cmds))
        self.conn.commit()

    def removeAlias(self, id, index):
        self.connection()
        try:
            sql = "DELETE FROM alias WHERE id_server= %s AND pattern =%s"
            self.mydb.execute(sql, (id,index))
            self.conn.commit()
        except:
            print("something wrong with removeAlias")


    def getAliases(self, id, pattern):
        self.connection()
        sql = "SELECT command FROM alias WHERE id_server= %s AND pattern=%s"
        self.mydb.execute(sql, (id,pattern))
        try:
            data = self.mydb.fetchone()
            cmds=data[0]
            return cmds.split('\n')
        except:
            return None

    def showAlias(self, id, index):
        self.connection()
        sql = "SELECT pattern,command FROM alias WHERE id_server= %s"
        self.mydb.execute(sql, (id,))
        data = self.mydb.fetchall()
        payload = []
        content = {}
        if(index is not -1):
            data = (data[index],)
        for result in data:
            content = {'pattern': result[0], 'cmds': result[1]}
            payload.append(content)
            content = {}
        return json.dumps(payload)


    """Configuration"""
    def getConfiguration(self, serverId):
        self.connection()
        sql= "SELECT * FROM configuration WHERE id_server = %s"
        self.mydb.execute(sql, (serverId,))
        try:
            data = self.mydb.fetchone()
            return data
        except:
            return None
