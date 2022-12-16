from ast import Store
from odoo import api, models, fields, exceptions
import logging
_logger = logging.getLogger(__name__)


class StorageMaterials(models.Model):
    _name = 'agriculture.storagematerials'
    _description = 'All materials in Storage'
    _rec_name = 'CropVarieties'

    # 米種的名稱
    CropVarieties = fields.Char("CropVarieties", required=True)
    # 米種存放的倉庫編號，從agriculture.storage建立。
    StorageId = fields.Many2one(
        'agriculture.storage', required=False)  # 存放的倉庫編號
    # 米種的重量
    CropWeights = fields.Float(
        "CropWeights", compute='_compute_checkout', inverse='_checkout', store=True)
    # 取出米種的重量
    Checkout = fields.Float("Checkout", default=0.0)

    @api.depends('Checkout')
    def _compute_checkout(self):
        for record in self:
            if record.CropWeights <= 0.0:
                pass
            elif record.CropWeights < record.Checkout:
                t = record.Checkout - record.CropWeights
                raise exceptions.ValidationError(
                    f"Sorry, Checkout weight cannot be bigger CropWeight. Over {t} kg")
            else:
                record.CropWeights = record.CropWeights - record.Checkout
        # _logger.info(f"this is cvs {cvs}")

    def _checkout(self):
        for rec in self:
            rec.Checkout = 0
