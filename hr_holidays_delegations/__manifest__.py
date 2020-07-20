# -*- coding: utf-8 -*-
{
    'name': "Leave Delegations",

    'summary': """
        Access Rights Delegation Link with leaves
        """,

    'author': "Appness Tech.",
    'website': "http://www.app-ness.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'custom',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['delegations', 'hr_holidays'],
    'auto_install': True,
    # always loaded
    'data': [
        'views/hr_leave_views.xml',
    ]
}