# -*- coding: utf-8 -*-
{
    'name': "Delivery Based Invoicing",
    'description': """
        This module enables you to link the invoice to outgoing shipment.
    """,
    'author': "Appness Technology Co.Ltd.",
    'website': "http://www.app-ness.com",
    'category': 'account',
    'version': '13.1.0.1',
    'depends': ['sale_management', 'sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_make_invoice_views.xml',
        'views/account_views.xml',
    ],
    'auto_install': True,
    'images': [
        'static/description/sale_delivery_invoicing.png',
    ]
}