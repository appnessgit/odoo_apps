# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError


class Leave(models.Model):
    _inherit = "hr.leave"

    delegate_employee_id = fields.Many2one('hr.employee', string="Delegate Access Rights To")
    delegation_id = fields.Many2one('hr.delegation', string="Related Delegation")

    def write(self, values):
        super(Leave, self).write(values)
        if values.get('state') and values.get('state') == 'validate':
            self._create_designation()

    def _create_designation(self):
        for rec in self:
            if not rec.delegate_employee_id:
                continue

            delegation_object = self.env['hr.delegation'].sudo()
            delegation = rec.sudo().delegation_id

            values = {
                'employee_id': rec.employee_id.id,
                'employee_grant_id': rec.delegate_employee_id.id,
                'date_from': rec.request_date_from,
                'date_to': rec.request_date_to,
            }

            if delegation:
                delegation.action_draft()
                delegation.write(values)
            else:
                delegation = delegation_object.create(values)
                message = _("This record has been created from: %s") % (",".join(
                    ["<a href=# data-oe-model=hr.leave data-oe-id=" + str(
                        rec.id) + ">" + rec.display_name + "</a>"]))
                delegation.message_post(body=message)

            delegation.onchange_employee_id()
            delegation.onchange_employee_grant_id()
            rec.delegation_id = delegation
