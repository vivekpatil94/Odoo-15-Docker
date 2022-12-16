from pkg_resources import require
from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)


class ArchivedAdditionalItem(models.Model):
    _name = 'agriculture.archived_additional_item'
    _description = 'Archived Additional Item'
    _rec_name = 'item_name'

    datetime = fields.Datetime('Date', required=True)
    item_name = fields.Char("Item Name", required=True)
    amount = fields.Float("Amount", default=1, required=False)
    unit_price = fields.Float("Price Per Unit", default=1, required=False)
    total_price = fields.Float("Total Price", default=1, required=True)

    item_kind = fields.Selection(
        selection=[('expenditure', '應付款項'), ('income', '應收款項')],
        string='Item Kind', required=True)

    drying_allowance = fields.Integer("Drying Allowance")
    transport_allowance = fields.Integer("Transport Allowance")

    interest = fields.Integer("Interest")
    comment = fields.Char("Comment")

    archived_id = fields.Many2one('agriculture.archived')

    @api.onchange('amount', 'unit_price')
    def _onchange_price(self):
        self.total_price = self.amount * self.unit_price

    @api.onchange('amount', 'total_price')
    def _onchange_unit_price(self):
        self.unit_price = self.total_price / self.amount
