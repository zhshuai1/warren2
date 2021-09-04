import MySQLdb as mysql
import MySQLdb.cursors


class StockSource:
    def __init__(self):
        self.sql_client = mysql.connect(host='localhost', port=3306, user='zhangsh', passwd='000000', db='stock',
                                        cursorclass=mysql.cursors.DictCursor)

    def get_all_stocks(self):
        with self.sql_client.cursor() as cursor:
            cursor.execute('select distinct(code) from stock')
            return cursor.fetchall()

    def get_stock_by_code(self, code, limit=500):
        with self.sql_client.cursor() as cursor:
            cursor.execute('select * from stock where code = %s order by date desc limit %s', (code, limit))
            return cursor.fetchall()
