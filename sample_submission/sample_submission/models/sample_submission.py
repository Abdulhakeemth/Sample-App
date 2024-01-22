# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SampleSubmission(models.Model):
    """Class defined for Sample Submission"""
    _name = 'sample.submission'
    _description = "Sample Submission model"

    reference = fields.Char(string="Reference", readonly=True, default=lambda self: _('New'))
    name = fields.Char(string="Name", help="Name of Sample", required=True)
    partner_id = fields.Many2one('res.partner', string="Customer", help="Name of the customer", required=True)
    date_of_submission = fields.Date(string="Date of Submission", default=fields.Date.today())
    description = fields.Text(string="Description")
    price = fields.Float(string="Price")
    discount = fields.Float(string="Discount")
    vat = fields.Float(string="VAT")
    state = fields.Selection([('pending', ' Pending'), ('doing', 'Doing'), ('completed', 'Completed')], default='pending', string="State")
    material_required_ids = fields.One2many('material.required.line', 'submission_id', string="Material Required")


    @api.model
    def create(self, vals_list):
        """Declaring function for creating unique sequence number
        for each submission"""
        if vals_list.get('reference', 'New') == 'New':
            vals_list['reference'] = self.env['ir.sequence'].next_by_code(
                'sample.submission.sequence') or 'New'
        result = super().create(vals_list)
        return result

    def sample_submission_invoice(self):
        """Declaring function for invoice wizard"""
        return {
            'name': 'Invoice confirmation',
            'type': 'ir.actions.act_window',
            'res_model': 'custom.invoice.confirmation.popup',
            'view_mode': 'form',
            'target': "new",
        }
    def add_materials(self):
        """Declaring function for material wizard"""
        return {
            'name': 'Material',
            'type': 'ir.actions.act_window',
            'res_model': 'material.required.wizard',
            'view_mode': 'form',
            'target': "new",
        }

class ConfirmationPopup(models.TransientModel):
    _name = 'custom.invoice.confirmation.popup'
    _description = 'Confirmation Popup'

    message = fields.Text(string='Message', readonly=True)

    def confirm_invoice(self):
        active_id = self._context.get('active_id')
        sample = self.env['sample.submission'].browse(active_id).exists()
        invoice = self.env['account.move'].create(
            {'move_type': 'out_invoice',
             'partner_id': sample.partner_id.id,
             'state': 'draft',
             'invoice_date': fields.Date.today()
             })
        for rec in sample.material_required_ids:
            line = self.env['account.move.line'].create({'product_id': rec.product_id.id,
                                                         'quantity': rec.quantity,
                                                         'move_id': invoice.id})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'move_type': 'out_invoice',
            'res_id': invoice.id,
            'target': 'current'
        }
