models_migration_config = {
    'res.partner.category': {
        'fields': ['id', 'active', 'color', 'create_date', 'write_date', 'name', 'parent_id/id',],
        'ignore_fields': ['parent_id/id'],
    },
    'res.partner': {
        'fields': ['id', 'active', 'name', 'phone', 'email', 'parent_id/id'],
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
}

partners_without_name_file_name = 'res.partner(no name).csv'
res_users_groups_file_name = 'res.users(groups).csv'
