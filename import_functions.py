from odoo_csv_tools import import_threaded

from models_migration_config import models_migration_config

GENERATED_CSV_FILES_PATH = 'generated_csv_files/'
IMPORT_DEFAULT_REQ_CONTEXT = {'tracking_disable' : True}
DEFAULT_WORKERS = 2
IMPORT_DEFAULT_BATCH_SIZE = 1000
IMPORT_CONNECTION_CONFIG_DIR = 'import_connection.conf'

def import_data(model_name = None, file_csv = None, context = None, separator = None,
                ignore_fields = None, group_by = None, workers = None, batch_size = None, absolute_file_path = None):
    model_migration_config = models_migration_config[model_name]
    if absolute_file_path:
        file_csv = absolute_file_path
    else:
      if file_csv:
          file_csv = f'{GENERATED_CSV_FILES_PATH}{file_csv}'
      elif not file_csv:
          file_csv = f'{GENERATED_CSV_FILES_PATH}{model_name}.csv'
    if not context:
        context = model_migration_config.get('context', IMPORT_DEFAULT_REQ_CONTEXT)
    if not separator:
        separator = model_migration_config.get('separator', ',')
    if not ignore_fields:
        ignore_fields = model_migration_config.get('ignore_fields', [])
    if not group_by:
        group_by = model_migration_config.get('group_by', False)
    if not workers:
        workers = model_migration_config.get('workers', DEFAULT_WORKERS)
    if not batch_size:
        batch_size = model_migration_config.get('batch_size', IMPORT_DEFAULT_BATCH_SIZE)

    if model_name == 'crm.lead.tag':
        model_name = 'crm.tag'

    import_threaded.import_data(
        IMPORT_CONNECTION_CONFIG_DIR,
        model_name,
        file_csv=file_csv,
        context=context,
        separator=separator,
        ignore=ignore_fields,
        split=group_by,
        max_connection=workers,
        batch_size=batch_size,
    )

def import_ignored_fields(model_name, fields = None, file_csv = None,  ignore_fields = [], group_by = [], workers = DEFAULT_WORKERS):
    model_migration_config = models_migration_config[model_name]
    if not fields:
        fields = model_migration_config['fields']
    ignore_fields = ignore_fields or model_migration_config.get('ignore_fields', [])
    if ignore_fields:
        # import the ignored fields
        added_fields = list(f for f in fields if f not in ignore_fields and f not in ['id'])
        import_data(model_name, file_csv=file_csv, ignore_fields=added_fields, group_by = group_by, workers = workers)
