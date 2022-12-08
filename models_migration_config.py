models_migration_config = {
    'res.partner.category': {
        'fields': ['id', 'active', 'color', 'create_date', 'write_date', 'name', 'parent_id/id',],
        'ignore_fields': ['parent_id/id'],
    },
    'res.partner': {
        'fields': ['id', 'active', 'name', 'phone', 'email', 'company_type', 'message_bounce', 'type', 'street', 'street2', 'city', 'zip', 'state_id/id', 'country_id/id', 'categ_id/id', 'parent_id/id'],
        'domain': ['|', ['active', '=', True], ['active', '=', False], ['name', '!=', False], ['name', '!=', '']],
        'ignore_fields': ['parent_id/id'],
    },
    'res.users': {
        'fields': ['id', 'active', 'login', 'email', 'name', 'partner_id/id', 'login_date', 'lang', 'tz', 'notification_type'],
        'domain': ['|', ['active', '=', True], ['active', '=', False], ['id', '>', 5]], # Skip Odoo's default users
    },
    'crm.lead.tag': {
        'fields': ['id', 'color', 'name']
    },
    'crm.stage': {
        'fields': ['id', 'fold', 'sequence', 'name'],
    },
    'crm.team': {
        'fields': ['id', 'name', 'active', 'user_id/id', 'alias_name', 'use_quotations', 'use_opportunities', 'use_leads', 'alias_contact', 'invoiced_target'],
        'domain': ['|', ['active', '=', True], ['active', '=', False]],
    },
     'crm.lead': {
        'fields': ['id', 'active', 'name', 'description', 'type', 'date_open', 'date_closed', 'message_bounce', 'priority', 'planned_revenue', 'probability', 'date_deadline', 'partner_name', 'street', 'street2', 'city', 'state_id/id', 'zip', 'country_id/id', 'website', 'partner_id/id', 'user_id/id', 'stage_id/id', 'team_id/id', 'tag_ids/id'],
        'domain': ['|', ['active', '=', True], ['active', '=', False]],
        'group_by': 'stage_id/id',
    },
    'mail.message': {
        'fields': ['id', 'res_id', 'model', 'message_type', 'body', 'subtype_id/id', 'message_id', 'subject', 'date', 'email_from', 'author_id/id', 'record_name', 'partner_ids/id', 'parent_id/id'],
        'domain': [['message_type', 'in', ['comment', 'email']], ['model', 'in', ['res.partner', 'crm.lead']]],#['model', '!=', 'calendar.event']], No permissions for calendar.events
    }

}

GENERATED_CSV_FILES_PATH = 'generated_csv_files/'
INPUT_CSV_FIILES_PATH = 'input_csv_files/'

partners_without_name_file_name = 'res.partner(no name).csv'
res_users_groups_file_name = 'res.users(groups).csv'
crm_team_members_file_name = 'crm.team(members).csv'
states_remapping_file_name = 'States Remapping - Input.csv'
