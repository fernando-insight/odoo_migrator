#!/usr/bin/env python

from odoo_csv_tools import import_threaded
from models_list import models

CONNECTION_CONFIG_DIR = 'import_connection_config'
REQ_CONTEXT = {'tracking_disable' : True}
CSV_FILES_PATH = 'csv_files/'

for model in models:
    import_threaded.import_data(CONNECTION_CONFIG_DIR,
                                model,
                                file_csv=f'{CSV_FILES_PATH}{model}.csv',
                                context=REQ_CONTEXT, separator=','
    )
#import_threaded.import_data()
