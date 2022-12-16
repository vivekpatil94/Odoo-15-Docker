from odoo import api, models, fields, exceptions
import logging
_logger = logging.getLogger(__name__)


class Storage(models.Model):
    _name = 'agriculture.storage'
    _description = 'Storage of agriculture app'
    _rec_name = 'StorageId'

    # 米種存放的倉庫編號
    StorageId = fields.Char(string='StorageId', required=True)
    # 有StorageId的每筆資料，從Materials抓取。
    Crops = fields.One2many(
        'agriculture.storagematerials', 'StorageId', string='Materials')

    # 每個StorageId裡 每一筆資料的米種 所有的
    CropVarieties = fields.Char(string='All CropVarieties')
    # 每個StorageId裡 每一筆資料的米重量 所有的
    CropWeights = fields.Char(
        string='All CropWeights', compute='_onchange_Crops', store=True)
    # 每個StorageId裡 所有資料的米種與米重 dictionary list
    myList = fields.Char(string='Materials')
    # 每個StorageId裡 所有資料的米總重
    TotalWeight = fields.Float('Total Weight')

    @api.depends('Crops.CropWeights', 'Crops.CropVarieties', 'Crops')
    def _onchange_Crops(self):
        cvWeight = []
        cv = []
        for rec in self:
            cvs = []  # 每個StorageId裡 每一筆資料的米種 所有的
            cvWeights = []  # 每個StorageId裡 每一筆資料的米重量 所有的
            for crop in rec.Crops:
                cvs.append(crop.CropVarieties)
                cvWeights.append(crop.CropWeights)

            rec.CropVarieties = cvs
            rec.CropWeights = cvWeights

            # _logger.info(f"this is storage {cvs}")

            content_list = {}  # 每個StorageId裡 所有資料的米種與米重 dictionary list
            for (name, weight) in zip(cvs, cvWeights):
                if name in content_list.keys():
                    # if the value is already in list, add current weight to the sum
                    content_list[name] += weight
                else:
                    # if the value is not yet in list, create an entry
                    content_list[name] = weight
            rec.myList = content_list
            rec.TotalWeight = sum(cvWeights)  # 每個StorageId裡 所有資料的米總重

    # # 限制StorageId不能重複
    @api.constrains('StorageId')
    def _check_Storage_id(self):
        storage_rec = self.env['agriculture.storage'].search(
            [('StorageId', '=', self.StorageId), ('id', '!=', self.id)])
        if storage_rec:
            raise exceptions.ValidationError(
                'Sorry, StorageId already Exists')
