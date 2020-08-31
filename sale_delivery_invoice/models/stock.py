# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    fully_invoiced = fields.Boolean("Fully Invoiced", compute='get_invoicing_state', store=True)

    @api.depends('move_ids_without_package.quantity_done',
                 'move_ids_without_package.qty_invoiced',
                 'move_ids_without_package.sale_line_id.qty_invoiced',
                 'move_ids_without_package.sale_line_id.qty_delivered'
                 )
    def get_invoicing_state(self):
        for record in self:
            record.fully_invoiced = all(move.qty_invoiced >= move.quantity_done
                                        for move in record.move_ids_without_package)
            # \
                                    # or \
                                    # all(line.qty_invoiced >= line.qty_delivered for line in
                                    #     record.move_ids_without_package.mapped('sale_line_id'))


class StockMove(models.Model):
    _inherit = 'stock.move'

    qty_invoiced = fields.Float("Invoiced Qty", compute="get_qty_invoiced", store=True)
    account_move_line_ids = fields.One2many('account.move.line.stock.move', 'stock_move_id', "Invoice Lines")

    @api.depends('account_move_line_ids.quantity', 'account_move_line_ids.state')
    def get_qty_invoiced(self):
        for record in self:
            invoice_lines = record.account_move_line_ids.filtered(lambda l: l.state not in ['cancel'])
            quantity = 0
            for line in invoice_lines:
                if line.type == 'out_invoice':
                    quantity += line.quantity
                elif line.type == 'out_refund':
                    quantity -= line.quantity

            record.qty_invoiced = quantity
