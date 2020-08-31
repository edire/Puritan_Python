
import os
import pyodbc
import urllib
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime as dt



def CallODBC(db
            , driver='ODBC Driver 17 for SQL Server'
            , server='ins-prod.database.windows.net'
            , uid=os.environ.get('InsProdAdminUID')
            , pwd=os.environ.get('InsProdAdminPWD')
            , local_cred='no'
            , engine='alchemy'
            , **kwargs
            ):

    if local_cred=='yes':
        uid = ''
        pwd = ''
        trusted_conn = 'trusted_connection=yes'
    else:
        uid = f'UID={uid};'
        pwd = f'PWD={pwd};'
        trusted_conn = ''

    driver = f'DRIVER={driver};'
    server = f'SERVER={server};'
    database = f'DATABASE={db};'
    raw_con = driver + server + database + trusted_conn + uid + pwd

    if engine == 'alchemy':
        conn_str = urllib.parse.quote_plus(raw_con)
        return create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn_str), fast_executemany=True)
    elif engine == 'pyodbc':
        return pyodbc.connect(raw_con)


def RunSQL(db, sql, **kwargs):
    conn = CallODBC(db=db, engine='pyodbc', **kwargs)
    with conn.cursor() as cursor:
        cursor.execute(sql)
        conn.commit()


def ReadSQL(db, sql, **kwargs):
    conn = CallODBC(db=db, engine='pyodbc', **kwargs)
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



# df = ReadSQL('Insurance', 'select top 10 * from dim.tblTime')
# df.info()

# con = CallODBC('Insurance')
# df.to_sql('tblTimeTest', con=con, schema='stage', index=False)

# df = ReadSQL('Insurance', 'select * from stage.tblTimeTest')
# df.info()

# RunSQL('Insurance', 'drop table stage.tblTimeTest')

# df = ReadSQL('Insurance', 'select * from stage.tblTimeTest')



# df = ReadSQL('MyFinance', 'select top 10 * from mid.tblTransactionsMint', server='localhost', local_cred='yes')
# df.info()

# con = CallODBC('MyFinance', server='localhost', local_cred='yes')
# df.to_sql('tblTimeTest', con=con, schema='stg', index=False)

# df = ReadSQL('MyFinance', 'select * from stg.tblTimeTest', server='localhost', local_cred='yes')
# df.info()

# RunSQL('MyFinance', 'drop table stg.tblTimeTest', server='localhost', local_cred='yes')

# df = ReadSQL('MyFinance', 'select * from stg.tblTimeTest', server='localhost', local_cred='yes')
