# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models
from odoo.tools.translate import _
import logging
import requests

_logger = logging.getLogger(__name__)


class Crop(models.Model):
    _name = "agriculture.crop"
    _inherit = 'mail.thread'
    _rec_name = 'SeqNumber'
    _description = "Crop"
    _order = "LastCreationTime desc"

    # ******主要使用資料******
    # ******流水號******
    SeqNumber = fields.Char(
        "SeqNumber",  required=False, readonly=True)
    # ******農夫的資訊從member中取得******
    SellerName = fields.Many2one(
        "agriculture.member", string="SellerName", required=False)
    SellerId = fields.Char(
        "SellerId", related="SellerName.SellerId", required=False)

    Region = fields.Char(
        "Region", related="SellerName.Region", required=False)
    AuxId = fields.Char("AuxId", related="SellerName.AuxId", required=False)
    FarmerType = fields.Selection(
        "FarmerType", related="SellerName.FarmerType", required=False)
    # *******************************************
    # ******農作物資料******
    FarmingMethod = fields.Selection([('conventional', '慣行農法'), (
        'organic', '有機耕作')], string='FarmingMethod', required=False)

    CropVariety = fields.Many2one(
        'agriculture.cropvariety', string='CropVariety', required=False)  # 品種 不同品種有不同的加成

    CropVariety_bonus = fields.Integer(
        'CropVariety_bonus', related="CropVariety.CropVariety_bonus", required=False)  # 品種加成bonus

    CropStatus = fields.Selection(
        [('DRY', '乾穀'), ('WET', '濕穀')], 'CropStatus', required=False)  # 乾穀 濕穀

    CropType = fields.Selection([('a', '越光米'), (
        'b', '紅/黑糯米'), ('c', '糯米')], string='CropType', required=False)  # 特殊米種

    isTGAP = fields.Boolean(
        string="isTGAP", default=False)  # 是否TAGP yes = +100

    FarmingAdaption = fields.Selection(
        [('a', '有機轉型'), ('b', '隔離帶')], string='FarmingAdaption', required=False)  # 農業轉型

    BrownYield = fields.Float(
        'BrownYield', required=True, default=0.0)  # 糙米成品率

    HullYield = fields.Float('HullYield', required=True,
                             default=0.0)  # 粗糠成品率

    BranYield = fields.Float('BranYield', required=True,
                             default=0.0)  # 米糠成品率

    PrimeYield = fields.Float(
        'PrimeYield', required=True, default=0.0)  # 白米成品率

    BBRiceYield = fields.Float(
        'BBRiceYield', required=True, default=0.0)  # 大碎米成品率

    SBRiceYield = fields.Float(
        'SBRiceYield', required=True, default=0.0)  # 小碎米成品率

    RawHumidity = fields.Float(
        'RawHumidity', required=True, default=0.0)  # 稻穀濕度

    RHafterDryer = fields.Float(
        'RHafterDryer', required=True, default=0.0)  # 烘乾後濕度

    BrownHumidity = fields.Float(
        'BrownHumidity', required=True, default=0.0)  # 糙米濕度

    RiceHumidity = fields.Float(
        'RiceHumidity', required=True, default=0.0)  # 白米濕度

    BrownIntactRatio = fields.Float(
        'BrownIntactRatio', required=True, default=0.0)  # 糙米-完整粒

    BrownCrackedRatio = fields.Float(
        'BrownCrackedRatio', required=True, default=0.0)  # 糙米-胴裂粒

    BrownImmatureRatio = fields.Float(
        'BrownImmatureRatio', required=True, default=0.0)  # 糙米-未熟粒

    BrownPestsRatio = fields.Float(
        'BrownPestsRatio', required=True, default=0.0)  # 糙米-被害粒

    BrownColoredRatio = fields.Float(
        'BrownColoredRatio', required=True, default=0.0)  # 糙米-染色粒

    BrownDeadRatio = fields.Float(
        'BrownDeadRatio', required=True, default=0.0)  # 糙米-死米

    TasteRating = fields.Float(
        'TasteRating', required=True, default=0.0)  # 食味值

    Protein = fields.Float('Protein', required=True, default=0.0)  # 蛋白質含量

    BrownMoisture = fields.Float(
        'BrownMoisture', required=True, default=0.0)  # 遠紅外線-糙米濕度

    BrownAmylose = fields.Float(
        'BrownAmylose', required=True, default=0.0)  # 直鏈性澱粉含量

    VolumeWeight = fields.Float(
        'VolumeWeight', required=True, default=0.0)  # 容量重量

    CarCropWeight = fields.Float(
        'CarCropWeight', required=True, default=0.0)  # 重車重量

    CarWeight = fields.Float('CarWeight', required=True, default=0.0)  # 車重

    HarvestYear = fields.Integer(
        'HarvestYear', required=True, default=0)  # 收穫年份 民國年

    HarvestPeriod = fields.Integer(
        'HarvestPeriod', required=True, default=0)  # 期數

    LastCreationTime = fields.Datetime(
        'LastCreationTime')  # 收購時間

    CropWeight = fields.Float(
        'CropWeight', compute='_compute_crop_weight', store=True, required=True, default=0.0)  # 稻穀總重量

    RawTotalWeight = fields.Float(
        'RawTotalWeight', required=True, default=0.0)

    BrownWeight = fields.Float(
        'BrownWeight', required=True, default=0.0)  # 糙米總重量

    HullWeight = fields.Float(
        'HullWeight', required=True, default=0.0)  # 粗糠總重量

    BranWeight = fields.Float(
        'BranWeight', required=True, default=0.0)  # 米糠總重量

    PrimeWeight = fields.Float(
        'PrimeWeight', required=True, default=0.0)  # 白米總重量

    BBRiceWeight = fields.Float(
        'BBRiceWeight', required=True, default=0.0)  # 大碎米總重量

    SBRiceWeight = fields.Float(
        'SBRiceWeight', required=True, default=0.0)  # 小碎米總重量

    WasteRatio = fields.Float('WasteRatio', required=True, default=0.0)

    BuyPrice = fields.Float('BuyPrice', required=True, default=0.0)

    MachineTime = fields.Integer('MachineTime', required=True, default=0)

    MachineUses = fields.Integer('MachineUses', required=True, default=0)

    MachineStatus = fields.Char('MachineStatus', required=True, default='')

    TotalLoadWeight = fields.Float(
        'TotalLoadWeight', required=True, default=0.0)

    LastEditTime = fields.Datetime('LastEditTime')

    WhiteAmylose = fields.Float('WhiteAmylose', required=True, default=0.0)

    WhiteProtein = fields.Float('WhiteProtein', required=True, default=0.0)

    WhiteQEV = fields.Float('WhiteQEV', required=True, default=0.0)

    WhiteMoisture = fields.Float('WhiteMoisture', required=True, default=0.0)

    WhiteIntactRatio = fields.Float(
        'WhiteIntactRatio', required=True, default=0.0)

    WhiteColoredRatio = fields.Float(
        'WhiteColoredRatio', required=True, default=0.0)

    WhiteCrackedRatio = fields.Float(
        'WhiteCrackedRatio', required=True, default=0.0)

    WhiteDeadRatio = fields.Float('WhiteDeadRatio', required=True, default=0.0)

    WhiteImmatureRatio = fields.Float(
        'WhiteImmatureRatio', required=True, default=0.0)

    WhitePestsRatio = fields.Float(
        'WhitePestsRatio', required=True, default=0.0)

    WetDryRatio = fields.Float('WetDryRatio', required=True, default=0.0)

    DryingFee = fields.Float('DryingFee', required=True, default=0.0)

    StorageId = fields.Char('StorageId', required=False)  # 存放的倉庫編號
    DryerId = fields.Char('DryerId', required=False)  # 洗米機編號

    is_sp_type = fields.Boolean(string='is_sp_type', default=False)

    WetToDryRatio = fields.Float(
        string='WetToDryRatio', default=0.0)

    CropWeight_by_ratio = fields.Float('CropWeight_by_ratio', default=0.0)

    # ******次要資料******

    StartTime = fields.Datetime('Start Time', required=False)
    StartTime_Date = fields.Char('Start Time Date', required=False)
    StartTime_Time = fields.Char('Start Time Time', required=False)

    EndTime = fields.Datetime('End Time', required=False)
    EndTime_Date = fields.Char('End Time Date', required=False)
    EndTime_Time = fields.Char('End Time Time', required=False)

    # active = fields.Boolean("Active?", default=True)
    archived_id = fields.Many2one("agriculture.archived")

    # notification

    def create_notification(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Compute Crop Condition Successed'),
                'type': 'success',
                'sticky': False,
                'fadeout': 'slow',
                'next': {
                    'type': 'ir.actions.act_window_close',
                }
            }
        }

    # new state

    @ api.model
    def _default_stage(self):
        Stage = self.env['crop.stage']
        return Stage.search([("state", "=", "draft")], limit=1)

    @ api.model
    def _done_stage(self):
        Stage = self.env['crop.stage']
        return Stage.search([("state", "=", "done")], limit=1)

    @ api.model
    def _archived_stage(self):
        Stage = self.env['crop.stage']
        return Stage.search([("state", "=", "archived")], limit=1)

    stage_id = fields.Many2one('crop.stage', default=_default_stage,
                               copy=False, group_expand="_group_expand_stage_id")
    state = fields.Selection(related="stage_id.state")

    # ******計價資料*****
    # 以計算完成定價
    PriceState = fields.Selection(
        [('draft', '草稿'), ('done', '計價完成'), ('archived', '完成出單')], string='PriceState', default='draft')
    # 底價判斷   底價 / 百台斤
    FinalPrice = fields.Float(
        "FinalPrice (/百台斤)", compute="_compute_final_price", store=True)

    # 總價加成
    TotalPrice = fields.Float(
        "TotalPrice (新台幣)", compute="_compute_total_price", store=True)

    # 計價驗證資料
    ValidDocsRecived = fields.Boolean(string='ValidDocsRecived', default=False)

    # 議價
    nego_price = fields.Float('nego_price', default=0)

    @api.depends('CarCropWeight', 'CarWeight')
    def _compute_crop_weight(self):
        for crop in self:
            crop.CropWeight = crop.CarCropWeight - crop.CarWeight

    @ api.depends('FarmerType',
                  'CropType',
                  'FarmingMethod',
                  'CropVariety_bonus',
                  'VolumeWeight',
                  'PrimeYield',
                  'TasteRating',
                  'BrownIntactRatio',
                  'FarmingAdaption',
                  'isTGAP',
                  'nego_price',
                  'is_sp_type',
                  'CropWeight_by_ratio',
                  'ValidDocsRecived')
    def _compute_final_price(self):
        params = self.env['ir.config_parameter'].sudo()
        base_price = float(params.get_param('agriculture.BasePrice'))
        contracted_price = float(params.get_param(
            'agriculture.ContractedMemberPrice'))
        koshihikariRice_price = float(
            params.get_param('agriculture.KoshihikariRice'))
        glutinousRicePrice_BR = float(params.get_param(
            'agriculture.GlutinousRicePrice_BR'))
        glutinousRicePrice = float(params.get_param(
            'agriculture.GlutinousRicePrice'))
        organicRice_price = float(params.get_param('agriculture.OrganicRice'))
        volumeWeightIsOverAndEqualTo = float(params.get_param(
            'agriculture.VolumeWeightIsOverAndEqualTo'))
        primeYieldIsOverAndEqualTo = float(params.get_param(
            'agriculture.PrimeYieldIsOverAndEqualTo'))
        organicRiceExtra = float(params.get_param(
            'agriculture.OrganicRiceExtra'))
        organicTransOrIso = float(params.get_param(
            'agriculture.OrganicTransOrIso'))
        tgap_bonus = float(params.get_param('agriculture.tgap_bonus'))
        ffs = float(params.get_param('agriculture.ffs_VolumeWeightIsOver'))
        final_PrimeYieldIsOverAndEqualTo = float(params.get_param(
            'agriculture.final_PrimeYieldIsOverAndEqualTo'))
        multiplication = float(params.get_param('agriculture.multiplication'))

        for record in self:

            if self._check_nValue(record.VolumeWeight, record.PrimeYield, record.TasteRating, record.BrownIntactRatio, record.CropType, record.CropVariety.CropVariety_name):
                if record.FarmerType == 'contract':
                    # 契約農民
                    # 特殊米種
                    if record.CropType == 'a':
                        # 越光米2600
                        record.FinalPrice = base_price + contracted_price + koshihikariRice_price

                    elif record.CropType == 'b':
                        # 黑糯米或紅糯米 2400
                        record.FinalPrice = base_price + contracted_price + glutinousRicePrice_BR
                    elif record.CropType == 'c':
                        # 糯米1700
                        record.FinalPrice = base_price + contracted_price + glutinousRicePrice
                    else:
                        # 其他
                        # 有機米
                        if record.FarmingMethod == 'organic':
                            # record.TasteRating = 0
                            # record.BrownIntactRatio = 0
                            vw = True if record.VolumeWeight >= volumeWeightIsOverAndEqualTo else False
                            py = True if record.PrimeYield >= primeYieldIsOverAndEqualTo else False
                            if vw is True and py is True:
                                record.FinalPrice = base_price + contracted_price + \
                                    organicRice_price + organicRiceExtra
                            elif vw is True and py is False:
                                record.FinalPrice = base_price + contracted_price + organicRice_price
                            elif vw is False and py is False:
                                record.FinalPrice = base_price + contracted_price + organicRice_price
                        elif record.FarmingMethod == 'conventional' or record.FarmingMethod == False:
                            # 有機轉型或隔離帶2200
                            if record.PrimeYield is 0 or record.VolumeWeight is 0 or record.TasteRating is 0 or record.BrownIntactRatio is 0:
                                record.FinalPrice = 0

                            else:
                                if record.FarmingAdaption == 'a' or record.FarmingAdaption == 'b':
                                    record.FinalPrice = base_price + contracted_price + organicTransOrIso
                                else:
                                    # 慣行耕作
                                    compare_list = [self._get_taste_rating_level(record.TasteRating), self._get_volume_weight_level(
                                        record.VolumeWeight), self._get_brown_intact_ratio_level(record.BrownIntactRatio)]
                                    # _logger.info(
                                    #     f"This is compare_list: {compare_list}")
                                    min_value = min(compare_list)
                                    # _logger.info(
                                    #     f"This is min_value: {min_value}")
                                    if min_value != -1:
                                        bonus = self._get_compare_price(
                                            min_value, record.PrimeYield) + record.CropVariety_bonus
                                        # _logger.info(f"This is bonus: {bonus}")
                                        if record.isTGAP:
                                            record.FinalPrice = bonus + tgap_bonus
                                        else:
                                            record.FinalPrice = bonus
                                    else:
                                        if record.VolumeWeight < ffs:
                                            v = final_PrimeYieldIsOverAndEqualTo - record.PrimeYield
                                            bonus = base_price + contracted_price - multiplication * \
                                                v if record.PrimeYield < final_PrimeYieldIsOverAndEqualTo else base_price + contracted_price
                                            record.FinalPrice = bonus

                        else:
                            record.FinalPrice = 0

                else:
                    # 非契約農民
                    record.FinalPrice = base_price  # 增加 議價金額（正負）
            else:
                record.FinalPrice = 0
                record.PriceState = 'draft'
                self.stage_id = self._default_stage()

            # 加成
            record.FinalPrice = record.FinalPrice + record.nego_price
            unit_tw = record.CropWeight_by_ratio / 60
            record.TotalPrice = unit_tw * record.FinalPrice
            if record.TotalPrice != 0:
                # 新增勾選框，若勾選則不完成計價確認，不可出單
                if record.ValidDocsRecived == True:
                    record.PriceState = 'done'
                    record.stage_id = self._done_stage()
                    return self.create_notification()
                else:
                    record.PriceState = 'draft'
                    record.stage_id = self._default_stage()

    def _get_volume_weight_level(self, expValue):
        params = self.env['ir.config_parameter'].sudo()
        fs = float(params.get_param('agriculture.fs_VolumeWeightIsOver'))
        ss = float(params.get_param('agriculture.ss_VolumeWeightIsOver'))
        ts = float(params.get_param('agriculture.ts_VolumeWeightIsOver'))
        ffs = float(params.get_param('agriculture.ffs_VolumeWeightIsOver'))
        p_list = [fs, ss, ts, ffs]
        x1 = expValue - p_list[3]
        x2 = x1 - p_list[2] + p_list[3]
        x3 = x1 - p_list[1] + p_list[3]
        x4 = x1 - p_list[0] + p_list[3]

        lx1 = 1 if x1 >= 0 else -1
        lx2 = 1 if x2 >= 0 else 0
        lx3 = 1 if x3 >= 0 else 0
        lx4 = 1 if x4 >= 0 else 0

        return lx1 + lx2 + lx3 + lx4

    def _get_taste_rating_level(self, expValue):
        params = self.env['ir.config_parameter'].sudo()
        fs = float(params.get_param('agriculture.fs_TasteRatingIsOver'))
        ss = float(params.get_param('agriculture.ss_TasteRatingIsOver'))
        ts = float(params.get_param('agriculture.ts_TasteRatingIsOver'))
        ffs = float(params.get_param('agriculture.ffs_TasteRatingIsOver'))
        p_list = [fs, ss, ts, ffs]
        x1 = expValue - p_list[3]
        x2 = x1 - p_list[2] + p_list[3]
        x3 = x1 - p_list[1] + p_list[3]
        x4 = x1 - p_list[0] + p_list[3]

        lx1 = 1 if x1 >= 0 else -1
        lx2 = 1 if x2 >= 0 else 0
        lx3 = 1 if x3 >= 0 else 0
        lx4 = 1 if x4 >= 0 else 0

        return lx1 + lx2 + lx3 + lx4

    def _get_brown_intact_ratio_level(self, expValue):
        params = self.env['ir.config_parameter'].sudo()
        fs = float(params.get_param('agriculture.fs_BrownIntactRatioIsOver'))
        ss = float(params.get_param('agriculture.ss_BrownIntactRatioIsOver'))
        ts = float(params.get_param('agriculture.ts_BrownIntactRatioIsOver'))
        ffs = float(params.get_param('agriculture.ffs_BrownIntactRatioIsOver'))
        p_list = [fs, ss, ts, ffs]
        x1 = expValue - p_list[3]
        x2 = x1 - p_list[2] + p_list[3]
        x3 = x1 - p_list[1] + p_list[3]
        x4 = x1 - p_list[0] + p_list[3]

        lx1 = 1 if x1 >= 0 else -1
        lx2 = 1 if x2 >= 0 else 0
        lx3 = 1 if x3 >= 0 else 0
        lx4 = 1 if x4 >= 0 else 0

        return lx1 + lx2 + lx3 + lx4

    def _get_compare_price(self, min, PrimeYield):
        params = self.env['ir.config_parameter'].sudo()
        base_price = float(params.get_param('agriculture.BasePrice'))
        contracted_price = float(params.get_param(
            'agriculture.ContractedMemberPrice'))
        fs_bonus = float(params.get_param('agriculture.fs_bonus'))
        ss_bonus = float(params.get_param('agriculture.ss_bonus'))
        ts_bonus = float(params.get_param('agriculture.ts_bonus'))

        # base_price 1550
        if min == 4:
            bonus = base_price + contracted_price + fs_bonus
            return bonus
        elif min == 3:
            bonus = base_price + contracted_price + ss_bonus
            return bonus
        elif min == 2:
            bonus = base_price + contracted_price + ts_bonus
            return bonus
        elif min == 1:
            bonus = base_price + contracted_price
            return bonus

    def _check_nValue(self, VolumeWeight, PrimeYield, TasteRating, BrownIntactRatio, CropType, CropVariety):
        return True if VolumeWeight != 0 or PrimeYield != 0 or TasteRating != 0 or BrownIntactRatio != 0 or CropType != False or CropVariety != False else False

    @api.depends('FinalPrice', 'nego_price')
    def _compute_total_price(self):
        for rec in self:
            rec.TotalPrice = rec.TotalPrice

    @api.onchange('is_sp_type')
    def _onchange_is_sp_type(self):
        _logger.info('is_sp_type has been changed')
        for record in self:
            if record.is_sp_type == False:
                record.CropType = False
            else:
                record.CropVariety = False
                record.FarmingMethod = False
                record.FarmingAdaption = False
                record.TasteRating = 0
                record.BrownIntactRatio = 0
                record.PrimeYield = 0
                record.VolumeWeight = 0

    @api.onchange('CropStatus', 'RawHumidity', 'CropWeight')
    def _onchange_WetToDryRatio(self):
        for rec in self:
            if rec.CropStatus == 'DRY':
                rec.WetToDryRatio = 100
                rec.CropWeight_by_ratio = rec.CropWeight
            elif rec.CropStatus == 'WET':
                rec.WetToDryRatio = 100 - rec.RawHumidity + 8
                r = rec.WetToDryRatio/100
                rec.CropWeight_by_ratio = rec.CropWeight * r
            else:
                rec.WetToDryRatio = 0

    @api.onchange('ValidDocsRecived')
    def _onchange_ValidDocsRecived(self):
        for rec in self:
            if rec.ValidDocsRecived == False:
                rec.PriceState = 'draft'
                rec.stage_id = self._default_stage()

    def unlink_archiveItem(self):
        self.PriceState = 'done'
        self.stage_id = self._done_stage()

    def write(self, vals):
        _logger.info(f"this write is {fields}")
        vals['LastEditTime'] = datetime.now()
        key = 'archived_id'
        if key in vals:
            archivedId = vals[key]
            if archivedId == 0:
                self.PriceState = 'done'
                self.stage_id = self._done_stage()
            else:
                self.PriceState = 'archived'
                self.stage_id = self._archived_stage()
        return super(Crop, self).write(vals)

    def _get_seqNumber(self):
        url = "http://ec2-34-215-20-244.us-west-2.compute.amazonaws.com:58809/api/Record"

        data = {"CropStatus": ""}
        response = requests.post(url, json=data)
        # _logger.info(response.json().get('SeqNumber'))
        return response.json().get('SeqNumber')

    def _get_year_to_kmtyear(self):
        # get year to kmt year
        currentDateTime = datetime.now()
        date = currentDateTime.date()
        year = date.strftime("%Y")
        return int(year) - 1911

    def _get_year_to_period(self):
        # get year to period
        d = datetime.now()
        m = d.strftime("%m")
        return 1 if int(m) >= 1 and int(m) <= 9 else 2

    @api.model
    def create(self, fields):
        _logger.info(f"this write is {fields}")
        fields['SeqNumber'] = self._get_seqNumber()
        fields['HarvestYear'] = self._get_year_to_kmtyear()
        fields['HarvestPeriod'] = self._get_year_to_period()
        fields['LastCreationTime'] = datetime.now()

        return super(Crop, self).create(fields)

    def get_crop_name(self):
        if self.is_sp_type:
            return dict(self._fields['CropType'].selection).get(self.CropType) if self.CropType else ''
        else:
            return self.CropVariety.CropVariety_name if self.CropVariety else ''

    # @api.model
    # def default_get(self, fields):
    #     res = super(Crop, self).default_get(fields)
    #     return res
