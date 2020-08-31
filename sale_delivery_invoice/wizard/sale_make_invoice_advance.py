from odoo import fields, models, api
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    advance_payment_method = fields.Selection(selection_add=[('delivery', 'Based On Deliveries')])
    picking_ids = fields.Many2many('stock.picking', string="Deliveries")
    sale_id = fields.Many2one('sale.order', string="Sale Order", default=lambda self: self.get_default_sale())

    def get_default_sale(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        for order in sale_orders:
            return order.id

    def create_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        order = self.sale_id
        invoice_object = self.env['account.move'].sudo()

        if self.advance_payment_method == 'delivery':
            invoice_vals = {
                'invoice_origin': order.name,
                'invoice_user_id': order.user_id.id,
                'narration': order.note,
                'partner_id': order.partner_invoice_id.id,
                'fiscal_position_id': order.fiscal_position_id.id or order.partner_id.property_account_position_id.id,
                'partner_shipping_id': order.partner_shipping_id.id,
                'currency_id': order.pricelist_id.currency_id.id,
                'invoice_payment_ref': order.client_order_ref,
                'invoice_payment_term_id': order.payment_term_id.id,
                'team_id': order.team_id.id,
                'campaign_id': order.campaign_id.id,
                'medium_id': order.medium_id.id,
                'source_id': order.source_id.id,
                'picking_ids': self.picking_ids.ids
            }
            invoice = invoice_object.with_context(check_move_validity=False, default_type='out_invoice').create(invoice_vals)
            # invoice.get_lines_from_pickings()
            if self._context.get('open_invoices', False):
                return sale_orders.action_view_invoice()
            return {'type': 'ir.actions.act_window_close'}

        super(SaleAdvancePaymentInv, self).create_invoices()