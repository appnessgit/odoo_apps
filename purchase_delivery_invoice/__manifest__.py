# -*- coding: utf-8 -*-
{
    'name': "Delivery Based Billing",

    'description': """
        Generate vendor bill from delivery orders 
    """,
    'author': "Appness Technology Co.Ltd.",
    'website': "http://www.app-ness.com",
    'category': 'account',
    'version': '13.1.0.1',
    'depends': ['purchase_stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_views.xml',
    ],
    'auto_install': True,
    'images': [
        'static/description/purchase_delivery_invoicing.png',
    ]
}