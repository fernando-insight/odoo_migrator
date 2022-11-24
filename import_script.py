#!/usr/bin/env python

import os

from odoo_csv_tools import import_threaded
from models_migration_config import models_migration_config

CONNECTION_CONFIG_DIR = 'import_connection.conf'
REQ_CONTEXT = {'tracking_disable' : True}
CSV_FILES_PATH = 'csv_files/'
DEFAULT_BATCH_SIZE = 1000
DEFAULT_WORKERS = int(os.environ.get('DEFAULT_WORKERS', 2))

def import_data(model_name = None, file_csv = None, context = None, separator = None, ignore_fields = None, workers = None):
    if not file_csv:
        file_csv = f'{CSV_FILES_PATH}{model_name}.csv'
    if not context:
        context = REQ_CONTEXT
    if not separator:
        separator = ','
    if not ignore_fields:
        ignore_fields = []
    if not workers:
        workers = DEFAULT_WORKERS


    import_threaded.import_data(CONNECTION_CONFIG_DIR,
                                model_name,
                                file_csv=file_csv,
                                context=context,
                                separator=separator,
                                ignore=ignore_fields,
                                max_connection=workers,
    )

for model_name in models_migration_config:
    model_migration_config = models_migration_config[model_name]

    context = model_migration_config.get('context')
    separator = model_migration_config.get('separator')
    ignore_fields = model_migration_config.get('ignore_fields')

    import_data(model_name,
                context=context,
                separator=separator,
                ignore_fields=ignore_fields
    )

    if ignore_fields:
        # import the ignored fields
        added_fields = list(f for f in model_migration_config['fields'] if f not in ignore_fields and f not in ['id', 'name'])
        import_data(model_name,
                    context=context,
                    separator=separator,
                    ignore_fields=added_fields
        )
