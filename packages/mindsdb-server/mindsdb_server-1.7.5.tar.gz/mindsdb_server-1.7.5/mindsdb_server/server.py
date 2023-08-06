from mindsdb_server.namespaces.predictor import ns_conf as predictor_ns
from mindsdb_server.namespaces.datasource import ns_conf as datasource_ns
from mindsdb_server.namespaces.util import ns_conf as utils_ns
from mindsdb_server.shared_ressources import get_shared
import json
import os
import mindsdb
import logging
import sys

def start_server(from_tests=False, port=47334, storage_path=''):
    # by default werkzeug send all to stderr. Here is dividing by log-level to stderr and stdout.
    if not logging.root.handlers:
        rootLogger = logging.getLogger()

        outStream = logging.StreamHandler(sys.stdout)
        outStream.addFilter(lambda record: record.levelno <= logging.INFO)
        rootLogger.addHandler(outStream)

        errStream = logging.StreamHandler(sys.stderr)
        errStream.addFilter(lambda record: record.levelno > logging.INFO)
        rootLogger.addHandler(errStream)

    '''
    mindsdb.CONFIG.MINDSDB_STORAGE_PATH =  '/home/george/tmpsotre'
    mindsdb.CONFIG.MINDSDB_PREDICTORS_PATH = '/home/george/tmpsotre/pred'
    mindsdb.CONFIG.MINDSDB_DATASOURCES_PATH = '/home/george/tmpsotre/ds'
    mindsdb.CONFIG.MINDSDB_TEMP_PATH = '/home/george/tmpsotre/tmp'
    '''
    mindsdb.CONFIG.MINDSDB_STORAGE_PATH = os.path.join(os.getcwd(),'storage', storage_path)
    mindsdb.CONFIG.MINDSDB_PREDICTORS_PATH = os.path.join(mindsdb.CONFIG.MINDSDB_STORAGE_PATH,'predictors')
    mindsdb.CONFIG.MINDSDB_DATASOURCES_PATH = os.path.join(mindsdb.CONFIG.MINDSDB_STORAGE_PATH,'datasources')
    mindsdb.CONFIG.MINDSDB_TEMP_PATH = os.path.join(mindsdb.CONFIG.MINDSDB_STORAGE_PATH,'tmp')
    os.makedirs(mindsdb.CONFIG.MINDSDB_STORAGE_PATH, exist_ok=True)
    os.makedirs(mindsdb.CONFIG.MINDSDB_PREDICTORS_PATH, exist_ok=True)
    os.makedirs(mindsdb.CONFIG.MINDSDB_DATASOURCES_PATH, exist_ok=True)
    os.makedirs(mindsdb.CONFIG.MINDSDB_TEMP_PATH, exist_ok=True)
    #'''
    app, api = get_shared()

    api.add_namespace(predictor_ns)
    api.add_namespace(datasource_ns)
    api.add_namespace(utils_ns)

    # return only app for tests to use test_client
    if from_tests:
        return app
    
    app.run(debug=True, port=port, host='0.0.0.0')

if __name__ == '__main__':
    start_server()
