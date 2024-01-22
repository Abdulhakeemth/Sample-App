# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MaterialRequiredWizard(models.Model):
    """Class defined for Material Required Wizard"""
    _name = 'material.required.wizard'
    _description = "Material Required Wizard model"

    material_req_ids = fields.One2many('material.required.line', 'material_id', string="Material Required")

    def action_confirm(self):
        """Declaring a function for adding materials to the material request line"""
        active_id = self._context.get('active_id')
        sample = self.env['sample.submission'].browse(active_id).exists()
        if sample:
            for rec in self.material_req_ids:
                self.env['material.required.line'].create({'product_id': rec.product_id.id,
                                                           'quantity': rec.quantity, 'remarks': rec.remarks,
                                                           'submission_id': sample.id})
