models_migration_config = {
    'res.partner.category': {
        'fields': ['id', 'active', 'color', 'create_date', 'write_date', 'name', 'parent_id/id',],
        'ignore_fields': ['parent_id/id'],
    },
    'res.partner': {
        'fields': ['id', 'active', 'name', 'phone', 'email', 'customer', 'supplier', 'company_type', 'message_bounce', 'type', 'street', 'street2', 'city', 'zip', 'state_id/id', 'country_id/id', 'parent_id/id', 'user_id/id'],
        'domain': ['|', ['active', '=', True], ['active', '=', False], ['name', '!=', False], ['name', '!=', '']],
        'ignore_fields': ['parent_id/id', 'user_id/id'],
    },
    'res.company': {
    },
    'res.users': {
        'fields': ['id', 'active', 'login', 'email', 'name', 'partner_id/id', 'login_date', 'lang', 'tz', 'notification_type', 'branch_id/id', 'allow_branch_ids/id'],
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
        'workers': 1
    },
    'project.tags': {
        'fields': ['id', 'name']
    },
    'project.project': {
        'fields': ['id', 'active', 'name', 'color', 'user_id/id', 'sequence', 'privacy_visibility', 'partner_id/id', 'label_tasks', 'alias_name', 'alias_contact', 'resource_calendar_id/id', 'branch_id/id'],
        'workers': 1,
        'domain': ['|', ['active', '=', True], ['active', '=', False]],
    },
    'project.task.type': {
        'fields': ['id', 'name', 'description', 'fold', 'sequence', 'legend_blocked', 'legend_done', 'legend_normal', 'project_ids/id']
    },
    'project.task': {
        'fields': ['id', 'active', 'name', 'priority', 'description', 'color', 'stage_id/id', 'email_from', 'project_id/id', 'user_id/id', 'date_deadline', 'tag_ids/id', 'planned_hours', 'sequence', 'partner_id/id', 'date_assign', 'date_last_stage_update', 'parent_id/id'],
        'ignore_fields': ['parent_id/id'],
        'domain': ['|', ['active', '=', True], ['active', '=', False]],
        'workers': 1
    },
    'product.category': {
        'fields': ['id', 'name', 'property_cost_method', 'property_valuation', 'parent_id/id'],
        'ignore_fields': ['parent_id/id']
    },
    'product.uom.categ': {
        'fields': ['id', 'name'],
    },
    'uom.category': {
       # New Model name of product.uom.category
    },
    'uom.uom': {
        # New Model name of product.uom
    },
    'product.uom': {
        'fields': ['id', 'active', 'name', 'category_id/id', 'uom_type', 'rounding', 'factor', 'factor_inv'],
        'domain': ['|', ['active', '=', True], ['active', '=', False],
                   ['id', 'not in', [25, 26, 27, 28]]],  # We skip the Unsorted/Imported Units
    },
    'product.template': {
        'fields': ['id', 'name', 'active', 'default_code', 'categ_id/id', 'tracking', 'barcode', 'sale_ok', 'purchase_ok', 'sequence', 'can_be_expensed', 'type', 'invoice_policy', 'purchase_method', 'list_price', 'description', 'description_sale', 'description_purchase', 'responsible_id/id', 'create_uid/id', 'create_date', 'weight', 'volume', 'uom_id/id', 'uom_po_id/id'],
        'domain': ['|', ['active', '=', True], ['active', '=', False]],
    },
    'product.product': {
        'fields': ['id', 'name', 'active', 'product_tmpl_id/id'],
        'domain': ['|', ['active', '=', True], ['active', '=', False]],
    },
    'product.supplierinfo': {
        'fields': ['id', 'name/id', 'min_qty', 'price', 'delay', 'product_name', 'product_code', 'date_end', 'product_tmpl_id/id', 'product_uom/id'],
        'domain': [['name', '!=', False], ['name', '!=', '']]
    },
    'purchase.order': {
        'fields': ['id', 'name', 'origin', 'partner_id/id', 'state', 'partner_ref', 'date_order', 'date_planned', 'date_approve', 'buyer/id', 'invoice_status', 'notes']
    },
    'purchase.order.line': {
        'fields': ['id', 'name', 'partner_id/id', 'state', 'product_id/id', 'order_id/id', 'date_planned', 'product_qty', 'qty_received', 'qty_invoiced', 'product_uom/id', 'price_unit', 'taxes_id/id', 'price_subtotal']
    },
    'sale.order': {
        'fields': ['id', 'name', 'origin', 'partner_id/id', 'state', 'partner_shipping_id/id', 'partner_invoice_id/id', 'date_order', 'create_date', 'effective_date', 'confirmation_date', 'commitment_date', 'validity_date', 'team_id/id', 'user_id/id', 'invoice_status', 'note', 'picking_policy', 'amount_total', 'amount_tax', 'amount_untaxed']
    },
    'sale.order.line': {
        'fields': ['id', 'name', 'product_id/id', 'order_id/id', 'product_uom_qty', 'qty_invoiced', 'qty_delivered', 'product_uom/id', 'tax_id/id', 'price_unit', 'price_subtotal', 'price_tax', 'price_total']
    },
    'ir.sequence': {
        'fields': ['id', 'active', 'name', 'implementation', 'prefix', 'use_date_range', 'padding', 'number_increment'],
        'domain': ['|', ['active', '=', True], ['active', '=', False], ['code', 'in', ['purchase.order', 'sale.order']]]
    },
    'ir.sequence.date_range': {
        'fields': ['id', 'date_from', 'date_to', 'number_next_actual', 'sequence_id/id']
    },
    'mail.message': {
        'fields': ['id', 'res_id', 'model', 'message_type', 'body', 'subtype_id/id', 'message_id', 'subject', 'date', 'email_from', 'author_id/id', 'record_name', 'partner_ids/id', 'parent_id/id'],
        'domain': [['model', 'in', ['crm.lead', 'crm.team', 'res.partner', 'project.project', 'project.task', 'product.template', 'purchase.order', 'sale.order', 'sale.order.line']]]
    },
    'mail.tracking.value': {
        'fields': ['id', 'field', 'field_desc', 'field_type', 'mail_message_id/id', 'old_value_char', 'old_value_datetime', 'old_value_integer', 'old_value_monetary', 'old_value_float', 'old_value_text', \
                   'new_value_char', 'new_value_datetime', 'new_value_integer', 'new_value_monetary', 'new_value_float', 'new_value_text'],
    },
    'ir.attachment': {
        'fields': ['id', 'name', 'description', 'type', 'mimetype', 'create_uid/id', 'index_content', 'public', 'res_name', 'res_model', 'res_id']
    },
}
