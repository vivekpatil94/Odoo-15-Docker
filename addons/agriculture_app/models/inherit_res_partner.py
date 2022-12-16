from odoo import models, fields, api


class Inherit_res_partner(models.Model):
    _inherit = 'res.partner'

    is_agriculture_member = fields.Boolean(string='Is an Agriculture Member', default=False,
                                           help="Check if the contact is a agriculture_member, otherwise it is a person or company", required=False)

    Member = fields.Many2one("agriculture.member",
                             string="SellerName", required=False)

    SellerName = fields.Char(
        "SellerName", related="Member.SellerName", required=False)

    SellerId = fields.Char(
        "SellerId", related="Member.SellerId", required=False)

    @api.onchange('is_agriculture_member', 'Member')
    def onchange_is_member(self):
        if self.is_agriculture_member:
            self.name = self.SellerName
        else:
            self.name = ''
