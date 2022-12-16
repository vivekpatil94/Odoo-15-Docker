from odoo import models, fields


class CropVariety(models.Model):
    _name = 'agriculture.cropvariety'
    _inherit = 'mail.thread'
    _description = 'CropVariety of agriculture app'
    _rec_name = 'CropVariety_name'

    CropVariety_name = fields.Char(required=False)
    CropVariety_bonus = fields.Integer(required=False, default=0)
