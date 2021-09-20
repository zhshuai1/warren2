import MySQLdb as mysql
import MySQLdb.cursors


def test_mysql():
    db = mysql.connect(host='localhost', port=3306, user='zhangsh', passwd='000000', db='stock',
                       cursorclass=mysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute('select code,date,minute from stock where code =%s limit 1', ('sh600030',))
    print(cursor.fetchall())


if __name__ == '__main__':
    test_mysql()
