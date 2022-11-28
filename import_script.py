#!/usr/bin/env python

import os

from odoo_csv_tools import import_threaded
from models_migration_config import models_migration_config, partners_without_name_file_name, res_users_groups_file_name

CONNECTION_CONFIG_DIR = 'import_connection.conf'
REQ_CONTEXT = {'tracking_disable' : True}
CSV_FILES_PATH = 'csv_files/'
DEFAULT_WORKERS = int(os.environ.get('DEFAULT_WORKERS', 2))
DEFAULT_BATCH_SIZE = 1000

def import_data(model_name = None, file_csv = None, context = None, separator = None, ignore_fields = None, group_by = None, workers = None, batch_size = None):
    model_migration_config = models_migration_config[model_name]
    if file_csv:
        file_csv = f'{CSV_FILES_PATH}{file_csv}'
    elif not file_csv:
        file_csv = f'{CSV_FILES_PATH}{model_name}.csv'
    if not context:
        context = model_migration_config.get('context', REQ_CONTEXT)
    if not separator:
        separator = model_migration_config.get('separator', ',')
    if not ignore_fields:
        ignore_fields = model_migration_config.get('ignore_fields', [])
    if not workers:
        workers = DEFAULT_WORKERS
    if not batch_size:
        batch_size = model_migration_config.get('batch_size', DEFAULT_BATCH_SIZE)


    import_threaded.import_data(CONNECTION_CONFIG_DIR,
                                model_name,
                                file_csv=file_csv,
                                context=context,
                                separator=separator,
                                ignore=ignore_fields,
                                split=group_by,
                                max_connection=workers,
                                batch_size=batch_size,
    )

def import_ignored_fields(model_name, file_csv = None, ignore_fields = [], workers = DEFAULT_WORKERS):
    model_migration_config = models_migration_config[model_name]
    ignore_fields = ignore_fields or model_migration_config.get('ignore_fields', [])
    if ignore_fields:
        # import the ignored fields
        added_fields = list(f for f in model_migration_config['fields'] if f not in ignore_fields and f not in ['id'])
        import_data(model_name, file_csv=file_csv, ignore_fields=added_fields, workers = workers)


def res_partner_import():
    model_name = 'res.partner'
    #import partners without name
    import_data(model_name=model_name, file_csv=partners_without_name_file_name)
    #import the rest of the partners
    import_data(model_name=model_name)

    ignore_fields = ['id', 'name'] + models_migration_config['res.partner']['ignore_fields']
    import_ignored_fields(model_name, ignore_fields = ignore_fields, workers=1)
    import_ignored_fields(model_name, file_csv=partners_without_name_file_name, ignore_fields = ignore_fields, workers=1)

models_migration_config['res.partner']['import_override_function'] = res_partner_import

def res_users_import():
    model_name = 'res.users'
    import_data(model_name=model_name)
    import_data(model_name=model_name, ignore_fields=['groups_id'], file_csv=res_users_groups_file_name, workers=1, batch_size=1, context={'update_many2many': True})

models_migration_config['res.users']['import_override_function'] = res_users_import


for model_name in models_migration_config:
    model_migration_config = models_migration_config[model_name]
    if 'import_override_function' not in model_migration_config:
        ignore_fields = model_migration_config.get('ignore_fields')
        import_data(model_name)
        if ignore_fields:
            import_ignored_fields(model_name)
    else:
        # Call import_override_function instead of the standard export procedure
        model_migration_config['import_override_function']()
