import sys
import traceback

import pypyodbc as pypyodbc


class BaseODBC(object):

    def __init__(self, MdbFile):
        self.connStr = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=%s;' % MdbFile
        # print('connStr:' + connStr)
        self.conn = pypyodbc.connect(self.connStr)

    def get_cur(self):
        self.cur = self.conn.cursor()
        return self.cur

    def excsql(self, sql, errExit=True):
        print(sql)
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except:
            print(traceback.format_exc())
            if errExit:
                sys.exit(-1)

    def exc_list_sql(self, listsql, errExit=True):
        for sql in listsql:
            print('input sql:' + sql)
            try:
                self.cur.execute(sql)
            except:
                print(traceback.format_exc())
                if errExit:
                    sys.exit(-1)
        self.conn.commit()

    def close_all(self):
        self.cur.close()
        self.conn.close()
