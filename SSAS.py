

import os
import clr
from mymodules import MyLogging

logger = MyLogging.NewLogger(__file__)

logger.info('Preparing to import Tabular module.')
amo_path = os.path.join(os.path.dirname(__file__), 'MiscFiles', 'Microsoft.AnalysisServices.Tabular.DLL')
clr.AddReference(amo_path)
import Microsoft.AnalysisServices.Tabular as AMO
logger.info('All modules successfully imported.')


def ProcessTabular(db, server=None, uid=None, pwd=None):
    if server==None:
        server = 'asazure://westus.asazure.windows.net/verdetabular'
    if uid==None:
        uid = os.getenv('Azure_SSAS_UID')
    if pwd==None:
        pwd = os.getenv('Azure_SSAS_PWD')
    
    conn = f'Provider=MSOLAP;Data Source={server};Initial Catalog={db}; User ID={uid}; Password={pwd}'
    
    logger.info('Parameters defined, beginning AMO connection.')
    AMOServer = AMO.Server()
    AMOServer.Connect(conn)
    logger.info('Connected, begin tabular model refresh.')
    db = AMOServer.Databases[db]
    db.Model.RequestRefresh(AMO.RefreshType.Full)
    op_result = db.Model.SaveChanges()
    logger.info('Refresh complete, disconnecting.')
    AMOServer.Disconnect()
    
    if op_result.Impact.IsEmpty:
        logger.warning('No models were impacted by refresh.')
        raise Exception('Model was not processed!')
    logger.info('ProcessTabular Function complete.')