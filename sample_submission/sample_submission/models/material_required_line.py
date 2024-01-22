# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MaterialRequiredLine(models.Model):
    """Class defined for Material Required Line"""
    _name = 'material.required.line'
    _description = "Material Required Line model"

    sl_no = fields.Integer(string="Sl No", compute="_get_line_numbers")
    product_id = fields.Many2one('product.product',string="Material")
    quantity = fields.Float(string="Quantity")
    remarks = fields.Char(string="Remarks")
    submission_id = fields.Many2one('sample.submission')
    material_id = fields.Many2one('material.required.wizard')

    @api.depends('submission_id.material_required_ids')
    def _get_line_numbers(self):
        for line in self:
            no = 0
            line.sl_no = no
            for l in line.submission_id.material_required_ids:
                no += 1
                l.sl_no = no

