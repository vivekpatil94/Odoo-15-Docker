import math
from termios import OPOST
from odoo import api, models, fields, exceptions
import logging
from .pycnnum import num2cn
from datetime import datetime
_logger = logging.getLogger(__name__)


class Archived(models.Model):
    _name = 'agriculture.archived'
    _inherit = 'mail.thread'
    _rec_name = 'SellerName'
    _description = 'Archived'
    _order = "LastCreationTime desc"

    # 農民資料
    member = fields.Many2one(
        "agriculture.member", "Member", required=True)
    SellerName = fields.Char(
        "SellerName", related="member.SellerName")
    SellerId = fields.Char(
        "SellerId", related="member.SellerId")
    Region = fields.Char("Region", related="member.Region")
    FarmerType = fields.Selection(
        "FarmerType", related="member.FarmerType")
    ContractArea = fields.Float(
        "ContractArea", related="member.ContractArea")
    ChishangRArea = fields.Float(
        "ChishangRArea", related="member.ChishangRArea")
    TGAPArea = fields.Float(
        "TGAPArea", related="member.TGAPArea")
    OrganicVerifyDate = fields.Date(
        "OrganicVerifyDate", related="member.OrganicVerifyDate")
    OrganiCertifiedArea = fields.Float(
        "OrganiCertifiedArea", related="member.OrganiCertifiedArea")
    NonLeasedArea = fields.Float(
        "NonLeasedArea", related="member.NonLeasedArea")
    MaxPurchaseQTY = fields.Float(
        "MaxPurchaseQTY", related="member.MaxPurchaseQTY")

    # 帳號資料
    MemberBankAccount = fields.Char(
        compute='_compute_MemberBankAccount')
    MemberBankName = fields.Char(compute='_compute_MemberBankName')
    MemberBankAccountHolderName = fields.Char(
        compute='_compute_MemberBankAccountHolderName')

    @api.depends('member')
    def _compute_MemberBankAccount(self):
        for rec in self:
            self.MemberBankAccount = rec.member.get_bank_info()['acc_number']

    @api.depends('member')
    def _compute_MemberBankName(self):
        for rec in self:
            self.MemberBankName = rec.member.get_bank_info()['bank_name']

    @api.depends('member')
    def _compute_MemberBankAccountHolderName(self):
        for rec in self:
            self.MemberBankAccountHolderName = rec.member.get_bank_info()[
                'acc_holder_name']
    ##########

    # 成單的序號列表
    seq_numbers = fields.One2many(
        'agriculture.crop', 'archived_id', 'Numbers of CropRecord', required=True)

    # 額外的資訊
    additional_items = fields.One2many(
        'agriculture.archived_additional_item', 'archived_id', 'Extra Items')

    # 單據時間
    LastCreationTime = fields.Datetime(
        'LastCreationTime', default=datetime.now())

    # 計算資料
    TotalExpenditure = fields.Float(compute='_compute_TotalExpenditure')
    TotalIncome = fields.Float(compute='_compute_TotalIncome')
    TotalActuallyPaid = fields.Float(compute='_compute_TotalActuallyPaid')
    TotalQTY = fields.Float(compute='_compute_TotalQTY')
    RemianingQTY = fields.Float(compute='_compute_RemianingQTY')
    IsOverflowQTY = fields.Boolean(compute='_compute_IsOverflowQTY')

    @api.depends('seq_numbers')
    def _compute_TotalQTY(self):
        for rec in self:
            rec.TotalQTY = 0
            for crop in rec.seq_numbers:
                rec.TotalQTY += crop.CropWeight

    @api.depends('TotalQTY', 'MaxPurchaseQTY')
    def _compute_RemianingQTY(self):
        for rec in self:
            rec.RemianingQTY = rec.MaxPurchaseQTY - rec.TotalQTY

    @api.onchange('RemianingQTY')
    def _compute_IsOverflowQTY(self):
        for rec in self:
            rec.IsOverflowQTY = rec.RemianingQTY < 0

    @api.depends('seq_numbers', 'additional_items')
    def _compute_TotalExpenditure(self):
        for rec in self:
            rec.TotalExpenditure = 0
            for crop in rec.seq_numbers:
                rec.TotalExpenditure += crop.TotalPrice
            for item in rec.additional_items:
                if item.item_kind == 'expenditure':
                    rec.TotalExpenditure += item.total_price
            rec.TotalExpenditure = math.floor(rec.TotalExpenditure)

    @api.depends('additional_items')
    def _compute_TotalIncome(self):
        for rec in self:
            rec.TotalIncome = 0
            for item in rec.additional_items:
                if item.item_kind == 'income':
                    rec.TotalIncome += item.total_price
            rec.TotalIncome = math.floor(rec.TotalIncome)

    @api.depends('TotalExpenditure', 'TotalIncome')
    def _compute_TotalActuallyPaid(self):
        for rec in self:
            rec.TotalActuallyPaid = math.floor(
                rec.TotalExpenditure - rec.TotalIncome)
    ##########

    @api.onchange('member')
    def _onchange_member(self):
        for seq in self.seq_numbers:
            if seq.SellerName.id != self.member.id:
                raise exceptions.ValidationError(
                    'Sorry, Seller\'s id not matched')

    def get_cn_num(self, input):
        return num2cn(math.floor(input), capitalize=True, traditional=True)

    def get_date(self, input):
        return "{:d}".format(input.year) + "/" + "{:0>2d}".format(input.month) + "/" + "{:0>2d}".format(input.day)

    def unlink(self):
        for seq in self.seq_numbers:
            seq.unlink_archiveItem()

        return super(Archived, self).unlink()


# 修正成單的序號刪除後，對應的成單也要刪除還原狀態

    @api.model
    def delete(self, vals):
        for seq in self.seq_numbers:
            seq.unlink_archiveItem()
