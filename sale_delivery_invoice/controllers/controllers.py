# -*- coding: utf-8 -*-
from odoo import http

# class SaleDeliveryInvoice(http.Controller):
#     @http.route('/sale_delivery_invoice/sale_delivery_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_delivery_invoice/sale_delivery_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_delivery_invoice.listing', {
#             'root': '/sale_delivery_invoice/sale_delivery_invoice',
#             'objects': http.request.env['sale_delivery_invoice.sale_delivery_invoice'].search([]),
#         })

#     @http.route('/sale_delivery_invoice/sale_delivery_invoice/objects/<model("sale_delivery_invoice.sale_delivery_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_delivery_invoice.object', {
#             'object': obj
#         })