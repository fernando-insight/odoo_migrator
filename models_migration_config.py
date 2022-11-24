models_migration_config = {
    'res.partner.category': {
        'ignore_fields': ['parent_id/id'],
        'fields': ['id', 'active', 'color', 'create_date', 'write_date', 'name', 'parent_id/id',]
    },
    'res.partner': {
        'fields': ['id', 'name', 'phone', 'email'],
        'domain': [['id', '<', '100']]
    },
}
