from odoo import fields, models


class CropStage(models.Model):
    _name = "crop.stage"
    _description = "crop record Stage"
    _order = "sequence"

    name = fields.Char()
    sequence = fields.Integer(default=10)
    fold = fields.Boolean()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [("draft", "Draft"), ("done", "Done"), ("archived", "Archived")], default="draft")
