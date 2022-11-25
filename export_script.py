#!/usr/bin/env python
import os
import pandas

from odoo_csv_tools import export_threaded
from models_migration_config import models_migration_config, partners_without_name_file_name

CONNECTION_CONFIG_DIR = 'export_connection.conf'
CSV_FILES_PATH = 'csv_files/'
DEFAULT_REQ_CONTEXT = {}
DEFAULT_BATCH_SIZE = 3000
DEFAULT_WORKERS = int(os.environ.get('DEFAULT_WORKERS', 2))

def export_data(model_name = None, domain = None, fields = None, output_file = None, workers = None, batch_size = None, context = None, separator = None):
    model_migration_config = models_migration_config[model_name]
    if not domain:
        domain = model_migration_config.get('domain', [])
    if not fields:
        fields = model_migration_config.get('fields', [])
    if output_file:
        output_file = f'{CSV_FILES_PATH}{output_file}'
    elif not output_file:
        output_file = f'{CSV_FILES_PATH}{model_name}.csv'
    if not workers:
        workers = DEFAULT_WORKERS
    if not batch_size:
        batch_size = model_migration_config.get('batch_size', DEFAULT_BATCH_SIZE)
    if not context:
        context = model_migration_config.get('context', DEFAULT_REQ_CONTEXT)
    if not separator:
        separator = model_migration_config.get('separator', ',')

    export_threaded.export_data(CONNECTION_CONFIG_DIR,
                                model_name,
                                domain,
                                fields,
                                output=output_file,
                                max_connection=workers,
                                batch_size=batch_size,
                                context=context,
                                separator=separator,
    )

def export_extra_function_res_partner_no_names():
    model_name = 'res.partner'
    model_migration_config = models_migration_config[model_name]

    fields_to_export = [f for f in model_migration_config['fields'] if f != 'name']
    export_data(model_name=model_name,
                domain=['|', ['name', '=', False], ['name', '=', '']],
                fields=fields_to_export,
                output_file=partners_without_name_file_name
    )
    partners_without_name_file_path = f'{CSV_FILES_PATH}{partners_without_name_file_name}'
    partners_dataframe = pandas.read_csv(partners_without_name_file_path)
    partners_dataframe.insert(len(fields_to_export), 'name','[N/A]')
    partners_dataframe.to_csv(partners_without_name_file_path, index=False)

models_migration_config['res.partner']['export_extra_functions'] = [export_extra_function_res_partner_no_names]


for model_name in models_migration_config:
    model_migration_config = models_migration_config[model_name]
    if 'export_override_function' not in model_migration_config:
        export_data(model_name=model_name)
        if 'export_extra_functions' in model_migration_config:
            # Call extra steps after exporting the csv file
            for extra_function in model_migration_config['export_extra_functions']:
                extra_function()
    else:
        # Call export_override_function instead of the standard export procedure
        model_migration_config['export_override_function']()
