
import os
import pyodbc
import urllib
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime as dt



def CallODBC(db, server='ins-prod.database.windows.net'):
    driver='DRIVER=ODBC Driver 17 for SQL Server;'
    server='SERVER=' + server + ';'
    database = 'DATABASE=' + db + ';'
    uid='UID=' + os.environ.get('InsProdAdminUID') + ';'
    pwd='PWD=' + os.environ.get('InsProdAdminPWD') + ';'
    conn_str = urllib.parse.quote_plus(driver + server + database + uid + pwd)
    return create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn_str), fast_executemany=True)
    

def CallODBC2(db, server='ins-prod.database.windows.net'):
    driver='DRIVER=ODBC Driver 17 for SQL Server;'
    server='SERVER=' + server + ';'
    database = 'DATABASE=' + db + ';'
    uid='UID=' + os.environ.get('InsProdAdminUID') + ';'
    pwd='PWD=' + os.environ.get('InsProdAdminPWD') + ';'
    conn_str = driver + server + database + uid + pwd
    return pyodbc.connect(conn_str)


def RunSQL(db, sql):
    conn = CallODBC2(db)
    with conn.cursor() as cursor:
        cursor.execute(sql)
        conn.commit()
    
    
def ReadSQL(db, sql):
    conn = CallODBC2(db)
    return pd.read_sql_query(sql=sql, con=conn)


def CallODBCAccess(dbq):
    driver='DRIVER=Microsoft Access Driver (*.mdb, *.accdb);'
    dbq='DBQ=' + dbq + ';'
    conn_str = driver + dbq
    return pyodbc.connect(conn_str)


def ReadSQLAccess(db, sql):
    conn = CallODBCAccess(db)
    return pd.read_sql_query(sql=sql, con=conn)


def RemoveWhitespace(x):
    if isinstance(x, str):
        return x.strip()
    else:
        return x


def DataCleanse(data):
    data.columns = data.columns.str.strip()
    data.columns = data.columns.str.replace('\"', '')
    data.columns = data.columns.str.replace('\'', '')
    data.columns = data.columns.str.replace('\\n', '_')
    data.columns = data.columns.str.replace(' ', '_')
    data = data.applymap(RemoveWhitespace)
    data = data.where(pd.notnull(data), None)
    data['RowLoadDateTime'] = dt.now()
    return data