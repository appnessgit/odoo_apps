# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    fully_billed = fields.Boolean("Fully Billed", compute='get_billing_state', store=True)

    @api.depends('move_ids_without_package.quantity_done',
                 'move_ids_without_package.qty_billed',
                 'move_ids_without_package.purchase_line_id.qty_invoiced',
                 'move_ids_without_package.purchase_line_id.qty_received'
                 )
    def get_billing_state(self):
        for record in self:
            record.fully_invoiced = all(move.qty_billed >= move.quantity_done
                                        for move in record.move_ids_without_package)
            # \
                                    # or \
                                    # all(line.qty_invoiced >= line.qty_received for line in
                                    #     record.move_ids_without_package.mapped('sale_line_id'))


class StockMove(models.Model):
    _inherit = 'stock.move'

    qty_billed = fields.Float("Invoiced Qty", compute="get_qty_billed", store=True)
    account_move_line_ids = fields.One2many('account.move.line.stock.move', 'stock_move_id', "Bill Lines")

    @api.depends('account_move_line_ids.quantity', 'account_move_line_ids.state')
    def get_qty_billed(self):
        for record in self:
            bill_lines = record.account_move_line_ids.filtered(lambda l: l.state not in ['cancel'])
            quantity = 0
            for line in bill_lines:
                if line.type == 'in_invoice':
                    quantity += line.quantity
                elif line.type == 'in_refund':
                    quantity -= line.quantity

            record.qty_billed = quantity
