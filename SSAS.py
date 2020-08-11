

import os
import clr

amo_path = os.path.join(os.path.dirname(__file__), 'MiscFiles', 'Microsoft.AnalysisServices.Tabular.DLL')
clr.AddReference(amo_path)
import Microsoft.AnalysisServices.Tabular as AMO



def ProcessTabular(db, server=None, uid=None, pwd=None):
    if server==None:
        server = 'asazure://westus.asazure.windows.net/verdetabular'
    if uid==None:
        uid = os.getenv('Azure_SSAS_UID')
    if pwd==None:
        pwd = os.getenv('Azure_SSAS_PWD')
    
    conn = f'Provider=MSOLAP;Data Source={server};Initial Catalog={db}; User ID={uid}; Password={pwd}'
    
    AMOServer = AMO.Server()
    AMOServer.Connect(conn)
    db = AMOServer.Databases['PythonRefreshTest']
    db.Model.RequestRefresh(AMO.RefreshType.Full)
    op_result = db.Model.SaveChanges()
    AMOServer.Disconnect()
    
    if op_result.Impact.IsEmpty:
        raise Exception('Model was not processed!')