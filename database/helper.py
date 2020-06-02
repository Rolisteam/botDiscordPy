#!/usr/bin/python3

import pymysql.cursors

def setShardCount(shardId, count):
    conn=pymysql.connect(host="localhost", user="renaud", passwd="hulan8ye", database="diceparser", charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            sql="UPDATE ShardCount SET guildcount = %s WHERE id = %s;"
            cursor.execute(sql, (count, shardId))
            conn.commit()
    finally:
        conn.close()



def computeTotalCount():
    conn=pymysql.connect(host="localhost", user="renaud", passwd="hulan8ye", database="diceparser", charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            sql="select sum(guildcount) as sum from ShardCount;"
            cursor.execute(sql)
            count = cursor.fetchone()
            return count['sum']
    finally:
        conn.close()
