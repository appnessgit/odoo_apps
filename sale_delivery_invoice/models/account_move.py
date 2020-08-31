from odoo import fields, models, api, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError
from collections import defaultdict


class AccountMoveLineMove(models.Model):
    _name = 'account.move.line.stock.move'
    _description = "Invoice Line Stock Move"
    _rec_name = 'stock_move_id'

    move_line_id = fields.Many2one('account.move.line', "Invoice Line")
    product_id = fields.Many2one('product.product', string="Product")
    stock_move_id = fields.Many2one('stock.move', 'Stock Move')
    quantity = fields.Float('Quantity', digits=(16, 2))
    state = fields.Selection(related='move_line_id.move_id.state')
    type = fields.Selection(related='move_line_id.move_id.type')


class AccountMove(models.Model):
    _inherit = 'account.move'

    picking_ids = fields.Many2many('stock.picking', 'picking_move_sale_rel', 'invoice_id', 'picking_id',
                                   string='Pickings', copy=False)

    @api.model
    def create(self, values):
        move = super(AccountMove, self).create(values)
        pickings = move.picking_ids
        if pickings:
            if not move.invoice_line_ids:
                move.get_lines_from_pickings()
            message = _("This invoice has been created from: %s") % (",".join(
                ["<a href=# data-oe-model=stock.picking data-oe-id=" + str(picking.id) + ">" + picking.name + "</a>" for
                 picking in pickings]))
            move.message_post(body=message)
        return move

    # Populate Invoice Lines from selected inventory transfers
    def get_lines_from_pickings(self):
        for record in self:
            record.invoice_line_ids.unlink()
            new_lines = record.env['account.move.line']
            pickings = record.picking_ids
            data = record._prepare_invoice_lines_from_picking(pickings)
            if data:
                for line in data:
                    line.pop('line_id', None)
                    new_line = new_lines.new(line)
                    new_lines += new_line

            record.invoice_line_ids = new_lines

            for line in record.invoice_line_ids:
                line.update(line._get_price_total_and_subtotal())
                line.update(line._get_fields_onchange_subtotal())

            record._onchange_invoice_line_ids()

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        super(AccountMove, self)._onchange_partner_id()
        self.picking_ids = False

    # Get Invoice Line values from stock.picking Object
    def _prepare_invoice_lines_from_picking(self, pickings):
        data = []
        lines = pickings.mapped('move_ids_without_package')

        for line in lines:
            remaining_qty = line.quantity_done - line.qty_invoiced

            sale_remaining = line.sale_line_id.qty_delivered - line.sale_line_id.qty_invoiced
            qty = min(remaining_qty, sale_remaining)

            if not qty:
                continue

            taxes = line.sale_line_id.tax_id
            invoice_line_tax_ids = line.sale_line_id.order_id.fiscal_position_id\
                .map_tax(taxes, line.sale_line_id.product_id, line.sale_line_id.order_id.partner_id)

            date = self.date or self.invoice_date
            line_data = {
                'sale_line_ids': [(6, 0, [line.sale_line_id.id])],
                'stock_move_ids': [(0, 0, {'stock_move_id': line.id, 'quantity': qty, 'product_id': line.product_id.id})],
                'name': line.name,
                'product_id': line.product_id.id,
                'account_id': line.product_id.product_tmpl_id.get_product_accounts()['income'].id,
                'price_unit': line.sale_line_id.order_id.currency_id._convert(
                    line.sale_line_id.price_unit, self.currency_id, line.sale_line_id.company_id,
                    date or fields.Date.today(), round=False),
                'quantity': qty,
                'discount': 0.0,
                'tax_ids': invoice_line_tax_ids.ids,
                'line_id': line.id
            }
            data.append(line_data)

        return data


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    stock_move_ids = fields.One2many('account.move.line.stock.move', 'move_line_id', string="Stock Moves")
    has_stock_moves = fields.Boolean(compute='compute_has_stock_moves', store=False)
    type = fields.Selection(related='move_id.type')

    @api.depends('stock_move_ids')
    def compute_has_stock_moves(self):
        for record in self:
            record.has_stock_moves = bool(record.stock_move_ids)
