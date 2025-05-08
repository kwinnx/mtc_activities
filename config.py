
# config.py
import pymysql

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '5533068'
DB_NAME = 'activities'
DB_CHARSET = 'utf8mb4'
#DB_CURSORCLASS = 'pymysql.cursors.DictCursor'


DB_CURSORCLASS = pymysql.cursors.DictCursor