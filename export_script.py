#!/usr/bin/env python
import os
import pandas
import numpy
import math

from odoo_csv_tools import export_threaded
from models_migration_config import GENERATED_CSV_FILES_PATH, INPUT_CSV_FIILES_PATH, models_migration_config, partners_without_name_file_name, \
    res_users_groups_file_name, crm_team_members_file_name, states_remapping_file_name

CONNECTION_CONFIG_DIR = 'export_connection.conf'
DEFAULT_REQ_CONTEXT = {}
DEFAULT_BATCH_SIZE = 3000
DEFAULT_WORKERS = int(os.environ.get('DEFAULT_WORKERS', 2))

def export_data(config = None, model_name = None, domain = None, fields = None, output_file = None, workers = None, batch_size = None, context = None, separator = None):
    if model_name == 'ir.model.data':
        model_migration_config = {}
    else:
        model_migration_config = models_migration_config[model_name]

    if not config:
        config = CONNECTION_CONFIG_DIR
    if not domain:
        domain = model_migration_config.get('domain', [])
    if not fields:
        fields = model_migration_config.get('fields', [])
    if output_file:
        output_file = f'{GENERATED_CSV_FILES_PATH}{output_file}'
    elif not output_file:
        output_file = f'{GENERATED_CSV_FILES_PATH}{model_name}.csv'
    if not workers:
        workers = DEFAULT_WORKERS
    if not batch_size:
        batch_size = model_migration_config.get('batch_size', DEFAULT_BATCH_SIZE)
    if not context:
        context = model_migration_config.get('context', DEFAULT_REQ_CONTEXT)
    if not separator:
        separator = model_migration_config.get('separator', ',')


    export_threaded.export_data(config,
                                model_name,
                                domain,
                                fields,
                                output=output_file,
                                max_connection=workers,
                                batch_size=batch_size,
                                context=context,
                                separator=separator,
    )

def export_extra_function_res_partner_clean_data():
    model_name = 'res.partner'

    partners_main_file_path = f'{GENERATED_CSV_FILES_PATH}{model_name}.csv'
    partners_dataframe = pandas.read_csv(partners_main_file_path)
    partners_dataframe.rename(columns={'categ_id/id': 'category_id/id'}, inplace=True)
    partners_dataframe['category_id/id'] = partners_dataframe['category_id/id'].str.replace('False', '')
    partners_dataframe['type'] = partners_dataframe['type'].str.replace('False', '')
    partners_dataframe['type'] = partners_dataframe['type'].str.replace('Shipping address', 'Delivery address')
    partners_dataframe.to_csv(partners_main_file_path, index=False)

def export_extra_function_res_partner_no_names():
    model_name = 'res.partner'
    model_migration_config = models_migration_config[model_name]

    fields_to_export = [f for f in model_migration_config['fields'] if f != 'name']
    export_data(model_name=model_name,
                domain=['|', ['name', '=', False], ['name', '=', '']],
                fields=fields_to_export,
                output_file=partners_without_name_file_name
    )
    partners_without_name_file_path = f'{GENERATED_CSV_FILES_PATH}{partners_without_name_file_name}'
    partners_dataframe = pandas.read_csv(partners_without_name_file_path)
    partners_dataframe.insert(len(fields_to_export), 'name','[N/A]')
    partners_dataframe.rename(columns={'categ_id/id': 'category_id/id'}, inplace=True)
    partners_dataframe['type'] = partners_dataframe['type'].str.replace('Shipping address', 'Delivery address')
    partners_dataframe.to_csv(partners_without_name_file_path, index=False)

def export_extra_function_res_partner_states_remapping():
    model_name = 'res.partner'

    partners_main_file_path = f'{GENERATED_CSV_FILES_PATH}{model_name}.csv'
    partners_dataframe = pandas.read_csv(partners_main_file_path)
    states_remapping_file_path = f'{INPUT_CSV_FIILES_PATH}{states_remapping_file_name}'
    states_remapping_dataframe = pandas.read_csv(states_remapping_file_path)

    #print(partners_dataframe['state_id/id']'state_us_3')
    for row in states_remapping_dataframe.itertuples():
        indexes = partners_dataframe[partners_dataframe['state_id/id'] == row.flash_hlg_state_id].index.tolist()
        for i in indexes:
            state_id = row.id if type(row.id) == str else ''
            partners_dataframe.loc[i:i, 'state_id/id': 'country_id/id'] = state_id, row.country_id

    partners_dataframe.to_csv(partners_main_file_path, index=False)

models_migration_config['res.partner']['export_extra_functions'] = [
    export_extra_function_res_partner_clean_data,
    export_extra_function_res_partner_no_names,
    export_extra_function_res_partner_states_remapping
]

def export_extra_function_res_users_groups():
    model_name = 'res.users'

    fields_to_export = ['id', 'groups_id', 'groups_id/id']
    export_data(model_name=model_name,
                fields=fields_to_export,
                output_file=res_users_groups_file_name,
    )
    res_users_groups_file_path = f'{GENERATED_CSV_FILES_PATH}{res_users_groups_file_name}'
    users_dataframe = pandas.read_csv(res_users_groups_file_path)
    users_dataframe.fillna(method='ffill', inplace=True)
    users_dataframe.to_csv(res_users_groups_file_path, index=False)

models_migration_config['res.users']['export_extra_functions'] = [export_extra_function_res_users_groups]

def export_extra_function_crm_team_members():
    model_name = 'crm.team'

    fields_to_export = ['id', 'member_ids', 'member_ids/id']
    export_data(model_name=model_name,
                fields=fields_to_export,
                output_file=crm_team_members_file_name
    )
    crm_team_file_path = f'{GENERATED_CSV_FILES_PATH}{crm_team_members_file_name}'
    crm_team_dataframe = pandas.read_csv(crm_team_file_path)
    crm_team_dataframe.fillna(method='ffill', inplace=True)
    crm_team_dataframe.to_csv(crm_team_file_path, index=False)

models_migration_config['crm.team']['export_extra_functions'] = [export_extra_function_crm_team_members]

def export_override_function_crm_lead():
    model_name = 'crm.lead'

    export_data(model_name=model_name)
    crm_lead_file_path = f'{GENERATED_CSV_FILES_PATH}{model_name}.csv'
    crm_lead_dataframe = pandas.read_csv(crm_lead_file_path)
    crm_lead_dataframe.rename(columns={'planned_revenue': 'expected_revenue'}, inplace=True)
    crm_lead_dataframe['priority'] = crm_lead_dataframe['priority'].str.replace('Low', 'Medium')
    crm_lead_dataframe['priority'] = crm_lead_dataframe['priority'].str.replace('Normal', 'Low')
    crm_lead_dataframe['tag_ids/id'] = crm_lead_dataframe['tag_ids/id'].str.replace('False', '')
    crm_lead_dataframe.to_csv(crm_lead_file_path, index=False)

models_migration_config['crm.lead']['export_override_function'] = export_override_function_crm_lead

def export_override_function_mail_message():
    model_name = 'mail.message'

    export_data(model_name=model_name)
    mail_message_file_path = f'{GENERATED_CSV_FILES_PATH}{model_name}.csv'
    mail_message_dataframe = pandas.read_csv(mail_message_file_path)

    mail_message_dataframe['subtype_id/id'] = mail_message_dataframe['subtype_id/id'].str.replace('False', '')

    models_with_mail_messages = list(mail_message_dataframe['model'].unique())
    models_to_export_external_ids = [m for m in models_with_mail_messages if m in models_migration_config.keys()]
    #Export external_ids
    fields_to_export = ['complete_name', 'res_id', 'model']
    export_data(model_name='ir.model.data',
                fields=fields_to_export,
                output_file='ir.model.data.old.csv',
                domain=[['model', 'in', models_to_export_external_ids]]
    )
    #Export v15 external_ids
    export_data(config='import_connection.conf',
                model_name='ir.model.data',
                fields=fields_to_export,
                output_file='ir.model.data.new.csv',
                domain=[['model', 'in', models_to_export_external_ids]]
    )
    external_ids_old_file_path = f'{GENERATED_CSV_FILES_PATH}ir.model.data.old.csv'
    external_ids_new_file_path = f'{GENERATED_CSV_FILES_PATH}ir.model.data.new.csv'
    merged_data_frame_file_path = f'{GENERATED_CSV_FILES_PATH}ir.model.data.merged.csv'
    ir_model_data_old_dataframe = pandas.read_csv(external_ids_old_file_path)
    ir_model_data_new_dataframe = pandas.read_csv(external_ids_new_file_path)
    # Merge old and new external ids to extract the new database id
    ir_model_data_old_dataframe.rename(columns={'res_id': 'old_res_id'}, inplace=True)
    ir_model_data_merged_dataframe = ir_model_data_new_dataframe.merge(ir_model_data_old_dataframe, on=['complete_name', 'model'], how='left')
    ir_model_data_merged_dataframe.rename(columns={'res_id': 'new_res_id'}, inplace=True)
    ir_model_data_merged_dataframe.to_csv(merged_data_frame_file_path, index=False)


    ir_model_data_merged_dataframe = pandas.read_csv(merged_data_frame_file_path)
    admin_partner_index = numpy.where(ir_model_data_merged_dataframe['complete_name'] == 'base.partner_admin')[0]
    template_user_partner_index = numpy.where(ir_model_data_merged_dataframe['complete_name'] == 'base.template_portal_user_id_res_partner')[0]

    # These partners can't be deleted so these ids won't change
    admin_old_res_id = 3
    template_user_res_id = 6
    ir_model_data_merged_dataframe['old_res_id'][admin_partner_index] = admin_old_res_id
    ir_model_data_merged_dataframe['old_res_id'][template_user_partner_index] = template_user_res_id
    ir_model_data_merged_dataframe['model'][admin_partner_index] = 'res.partner'
    ir_model_data_merged_dataframe['model'][template_user_partner_index] = 'res.partner'
    ir_model_data_merged_dataframe['old_res_id'] = ir_model_data_merged_dataframe['old_res_id'].astype('int')

    # Merge the mail.message dataframe with ir_model_data_merged_dataframe to get the new database ids
    mail_message_dataframe = mail_message_dataframe.merge(ir_model_data_merged_dataframe, left_on=['model', 'res_id'], right_on=['model', 'old_res_id'], how='inner')
    mail_message_dataframe.rename(columns={'res_id': 'old_res_id'}, inplace=True)
    mail_message_dataframe.rename(columns={'new_res_id': 'res_id'}, inplace=True)
    mail_message_dataframe['res_id'] = mail_message_dataframe['res_id'].astype('int')

    mail_message_dataframe.sort_values('date', ascending=True, inplace=True)
    mail_message_dataframe.to_csv(mail_message_file_path, index=False)

models_migration_config['mail.message']['export_override_function'] = export_override_function_mail_message


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
