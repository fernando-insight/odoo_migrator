#!/usr/bin/env python

from odoo_csv_tools import export_threaded
from models_list import models

CONNECTION_CONFIG = 'export_connection_config'
CSV_FILES_PATH = 'csv_files/'

for model in models:
    export_threaded.export_data(CONNECTION_CONFIG,
                                model,
                                models[model].get('domain', []),
                                models[model]['fields'],
                                output=f'{CSV_FILES_PATH}{model}.csv',
                                batch_size=1000,
                                context={},
                                separator=models[model].get('separator', ',')
    )
