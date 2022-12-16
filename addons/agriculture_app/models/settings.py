from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class Preferences(models.TransientModel):
    _inherit = 'res.config.settings'

    currency_id = fields.Many2one(
        'res.currency', string='Currency')

    # Fields
    # ----------------------------------------------------------
    # General
    BasePrice = fields.Monetary(
        string='Base Price', required=True, default=1400.0)

    ContractedMemberPrice = fields.Monetary(
        'Contracted Member Price', required=True, default=150.0)
    KoshihikariRice = fields.Monetary(
        'Koshihikari Rice', default=1050.0, required=True)
    GlutinousRicePrice_BR = fields.Monetary(
        'Glutinous Rice Price BR', default=850.0, required=True)
    GlutinousRicePrice = fields.Monetary(
        'Glutinous Rice Price', default=150.0, required=True)

    OrganicRice = fields.Monetary(
        'Organic Rice', default=750.0, required=True)
    VolumeWeightIsOverAndEqualTo = fields.Float(
        'Volume Weight Is Over And Equal To', default=620.0)
    PrimeYieldIsOverAndEqualTo = fields.Float(
        'Prime Yield Is Over And Equal To', default=70.0)
    OrganicRiceExtra = fields.Monetary(
        'Organic Rice Extra', default=300.0, required=True)

    OrganicTransOrIso = fields.Monetary(
        'OrganicTransOrIso', default=650.0, required=True)

    # first stage conditions
    # ----------------------------------------------------------
    fs_VolumeWeightIsOver = fields.Float(
        'Volume Weight Is Over', default=620.0)
    fs_TasteRatingIsOver = fields.Float('Taste Rating Is Over', default=73.0)
    fs_BrownIntactRatioIsOver = fields.Float(
        'Brown Intact Ratio Is Over', default=80.0)

    fs_bonus = fields.Monetary(
        'fs_bonus', default=180.0, required=True)

    # second stage conditions
    # ----------------------------------------------------------
    ss_VolumeWeightIsOver = fields.Float(
        'Volume Weight Is Over', default=590.0)
    ss_TasteRatingIsOver = fields.Float('Taste Rating Is Over', default=65.0)
    ss_BrownIntactRatioIsOver = fields.Float(
        'Brown Intact Ratio Is Over', default=70.0)

    ss_bonus = fields.Monetary(
        'ss_bonus', default=120.0, required=True)

    # third stage conditions
    # ----------------------------------------------------------
    ts_VolumeWeightIsOver = fields.Float(
        'Volume Weight Is Over', default=560.0)
    ts_TasteRatingIsOver = fields.Float('Taste Rating Is Over', default=64.0)
    ts_BrownIntactRatioIsOver = fields.Float(
        'Brown Intact Ratio Is Over', default=65)

    ts_bonus = fields.Monetary(
        'ts_bonus', default=60.0, required=True)

    # fourth stage conditions
    # ----------------------------------------------------------
    ffs_VolumeWeightIsOver = fields.Float(
        'Volume Weight Is Over', default=539.0)
    ffs_TasteRatingIsOver = fields.Float('Taste Rating Is Over', default=59.0)
    ffs_BrownIntactRatioIsOver = fields.Float(
        'Brown Intact Ratio Is Over', default=60)

    # TGAP bonus
    # ----------------------------------------------------------
    tgap_bonus = fields.Monetary(
        'TGAP bonus', default=100.0, required=True)

    final_PrimeYieldIsOverAndEqualTo = fields.Float(
        'Prime Yield Is Over And Equal To', default=70.0)

    # Final multiplication
    # ----------------------------------------------------------
    multiplication = fields.Float('Multiplication', default=20)

    maxPurchaseQTYPerHectare = fields.Float(
        'MaxPurchaseQTYPerHectare', default=6000.0)

    # Logistics configuration
    # ----------------------------------------------------------
    blackCat_customer_id = fields.Char('BlackCat_Customer_Id')
    blackCat_api_token = fields.Char('BlackCat_Api_Token')
    blackCat_api_url = fields.Char('BlackCat_Api_Url')

    # Logistics configuration print
    # ----------------------------------------------------------
    ecan_customer_id = fields.Char('Ecan_Customer_Id')
    ktj_customer_id = fields.Char('KTJ_Customer_Id')

    def set_values(self):
        '''agriculture setting field values'''
        res = super(Preferences, self).set_values()
        icp = self.env['ir.config_parameter']
        icp.set_param('agriculture.BasePrice', self.BasePrice)
        icp.set_param('agriculture.ContractedMemberPrice',
                      self.ContractedMemberPrice)
        icp.set_param('agriculture.KoshihikariRice', self.KoshihikariRice)
        icp.set_param('agriculture.GlutinousRicePrice_BR',
                      self.GlutinousRicePrice_BR)
        icp.set_param('agriculture.GlutinousRicePrice',
                      self.GlutinousRicePrice)
        icp.set_param('agriculture.OrganicRice', self.OrganicRice)
        icp.set_param('agriculture.VolumeWeightIsOverAndEqualTo',
                      self.VolumeWeightIsOverAndEqualTo)
        icp.set_param('agriculture.PrimeYieldIsOverAndEqualTo',
                      self.PrimeYieldIsOverAndEqualTo)
        icp.set_param('agriculture.OrganicRiceExtra', self.OrganicRiceExtra)
        icp.set_param('agriculture.OrganicTransOrIso', self.OrganicTransOrIso)
        icp.set_param('agriculture.fs_VolumeWeightIsOver',
                      self.fs_VolumeWeightIsOver)
        icp.set_param('agriculture.fs_TasteRatingIsOver',
                      self.fs_TasteRatingIsOver)
        icp.set_param('agriculture.fs_BrownIntactRatioIsOver',
                      self.fs_BrownIntactRatioIsOver)
        icp.set_param('agriculture.fs_bonus', self.fs_bonus)
        icp.set_param('agriculture.ss_VolumeWeightIsOver',
                      self.ss_VolumeWeightIsOver)
        icp.set_param('agriculture.ss_TasteRatingIsOver',
                      self.ss_TasteRatingIsOver)
        icp.set_param('agriculture.ss_BrownIntactRatioIsOver',
                      self.ss_BrownIntactRatioIsOver)
        icp.set_param('agriculture.ss_bonus', self.ss_bonus)
        icp.set_param('agriculture.ts_VolumeWeightIsOver',
                      self.ts_VolumeWeightIsOver)
        icp.set_param('agriculture.ts_TasteRatingIsOver',
                      self.ts_TasteRatingIsOver)
        icp.set_param('agriculture.ts_BrownIntactRatioIsOver',
                      self.ts_BrownIntactRatioIsOver)
        icp.set_param('agriculture.ts_bonus', self.ts_bonus)
        icp.set_param('agriculture.ffs_VolumeWeightIsOver',
                      self.ffs_VolumeWeightIsOver)
        icp.set_param('agriculture.ffs_TasteRatingIsOver',
                      self.ffs_TasteRatingIsOver)
        icp.set_param('agriculture.ffs_BrownIntactRatioIsOver',
                      self.ffs_BrownIntactRatioIsOver)
        icp.set_param('agriculture.tgap_bonus', self.tgap_bonus)
        icp.set_param('agriculture.final_PrimeYieldIsOverAndEqualTo',
                      self.final_PrimeYieldIsOverAndEqualTo)
        icp.set_param('agriculture.multiplication', self.multiplication)
        icp.set_param('agriculture.maxPurchaseQTYPerHectare',
                      self.maxPurchaseQTYPerHectare)
        '''Logistics configuration'''
        icp.set_param('agriculture.blackCat_customer_id',
                      self.blackCat_customer_id),
        icp.set_param('agriculture.blackCat_api_token',
                      self.blackCat_api_token),
        icp.set_param('agriculture.blackCat_api_url',
                      self.blackCat_api_url)

        icp.set_param('agriculture.ecan_customer_id', self.ecan_customer_id)
        icp.set_param('agriculture.ktj_customer_id', self.ktj_customer_id)

        return res

    def get_values(self):
        '''agriculture limit getting field values'''
        res = super(Preferences, self).get_values()
        icp = self.env['ir.config_parameter']
        value_BasePrice = icp.sudo(
        ).get_param('agriculture.BasePrice', default=1400.0)
        value_ContractedMemberPrice = icp.sudo(
        ).get_param('agriculture.ContractedMemberPrice', default=150.0)
        value_KoshihikariRice = icp.sudo(
        ).get_param('agriculture.KoshihikariRice', default=1050.0)
        value_GlutinousRicePrice_BR = icp.sudo(
        ).get_param('agriculture.GlutinousRicePrice_BR', default=850.0)
        value_GlutinousRicePrice = icp.sudo(
        ).get_param('agriculture.GlutinousRicePrice', default=150.0)
        value_OrganicRice = icp.sudo(
        ).get_param('agriculture.OrganicRice', default=750.0)
        value_VolumeWeightIsOverAndEqualTo = icp.sudo(
        ).get_param('agriculture.VolumeWeightIsOverAndEqualTo', default=610.0)
        value_PrimeYieldIsOverAndEqualTo = icp.sudo(
        ).get_param('agriculture.PrimeYieldIsOverAndEqualTo', default=70)
        value_OrganicRiceExtra = icp.sudo(
        ).get_param('agriculture.OrganicRiceExtra', default=300.0)
        value_OrganicTransOrIso = icp.sudo(
        ).get_param('agriculture.OrganicTransOrIso', default=650.0)
        value_fs_VolumeWeightIsOver = icp.sudo(
        ).get_param('agriculture.fs_VolumeWeightIsOver', default=610.0)
        value_fs_TasteRatingIsOver = icp.sudo(
        ).get_param('agriculture.fs_TasteRatingIsOver', default=73)
        value_fs_BrownIntactRatioIsOver = icp.sudo(
        ).get_param('agriculture.fs_BrownIntactRatioIsOver', default=80)
        value_fs_bonus = icp.sudo(
        ).get_param('agriculture.fs_bonus', default=180.0)
        value_ss_VolumeWeightIsOver = icp.sudo(
        ).get_param('agriculture.ss_VolumeWeightIsOver', default=590.0)
        value_ss_TasteRatingIsOver = icp.sudo(
        ).get_param('agriculture.ss_TasteRatingIsOver', default=65)
        value_ss_BrownIntactRatioIsOver = icp.sudo(
        ).get_param('agriculture.ss_BrownIntactRatioIsOver', default=70)
        value_ss_bonus = icp.sudo(
        ).get_param('agriculture.ss_bonus', default=120.0)
        value_ts_VolumeWeightIsOver = icp.sudo(
        ).get_param('agriculture.ts_VolumeWeightIsOver', default=560.0)
        value_ts_TasteRatingIsOver = icp.sudo(
        ).get_param('agriculture.ts_TasteRatingIsOver', default=64)
        value_ts_BrownIntactRatioIsOver = icp.sudo(
        ).get_param('agriculture.ts_BrownIntactRatioIsOver', default=65)
        value_ts_bonus = icp.sudo(
        ).get_param('agriculture.ts_bonus', default=60.0)
        value_ffs_VolumeWeightIsOver = icp.sudo(
        ).get_param('agriculture.ffs_VolumeWeightIsOver', default=539.0)
        value_ffs_TasteRatingIsOver = icp.sudo(
        ).get_param('agriculture.ffs_TasteRatingIsOver', default=59)
        value_ffs_BrownIntactRatioIsOver = icp.sudo(
        ).get_param('agriculture.ffs_BrownIntactRatioIsOver', default=60)
        value_tgap_bonus = icp.sudo(
        ).get_param('agriculture.tgap_bonus', default=100.0)
        value_final_PrimeYieldIsOverAndEqualTo = icp.sudo(
        ).get_param('agriculture.final_PrimeYieldIsOverAndEqualTo', default=63)
        value_multiplication = icp.sudo(
        ).get_param('agriculture.multiplication', default=20.0)
        value_maxPurchaseQTYPerHectare = icp.sudo().get_param(
            'agriculture.maxPurchaseQTYPerHectare', default=6000.0)

        '''Logistics configuration'''
        value_blackCat_customer_id = icp.sudo().get_param(
            'agriculture.blackCat_customer_id')
        value_blackCat_api_token = icp.sudo().get_param('agriculture.blackCat_api_token')
        value_blackCat_api_url = icp.sudo().get_param('agriculture.blackCat_api_url')

        value_ecan_customer_id = icp.sudo().get_param('agriculture.ecan_customer_id')
        value_ktj_customer_id = icp.sudo().get_param('agriculture.ktj_customer_id')

        res.update(
            BasePrice=float(value_BasePrice),
            ContractedMemberPrice=float(value_ContractedMemberPrice),
            KoshihikariRice=float(value_KoshihikariRice),
            GlutinousRicePrice_BR=float(value_GlutinousRicePrice_BR),
            GlutinousRicePrice=float(value_GlutinousRicePrice),
            OrganicRice=float(value_OrganicRice),
            VolumeWeightIsOverAndEqualTo=float(
                value_VolumeWeightIsOverAndEqualTo),
            PrimeYieldIsOverAndEqualTo=float(value_PrimeYieldIsOverAndEqualTo),
            OrganicRiceExtra=float(value_OrganicRiceExtra),
            OrganicTransOrIso=float(value_OrganicTransOrIso),
            fs_VolumeWeightIsOver=float(value_fs_VolumeWeightIsOver),
            fs_TasteRatingIsOver=float(value_fs_TasteRatingIsOver),
            fs_BrownIntactRatioIsOver=float(value_fs_BrownIntactRatioIsOver),
            fs_bonus=float(value_fs_bonus),
            ss_VolumeWeightIsOver=float(value_ss_VolumeWeightIsOver),
            ss_TasteRatingIsOver=float(value_ss_TasteRatingIsOver),
            ss_BrownIntactRatioIsOver=float(value_ss_BrownIntactRatioIsOver),
            ss_bonus=float(value_ss_bonus),
            ts_VolumeWeightIsOver=float(value_ts_VolumeWeightIsOver),
            ts_TasteRatingIsOver=float(value_ts_TasteRatingIsOver),
            ts_BrownIntactRatioIsOver=float(value_ts_BrownIntactRatioIsOver),
            ts_bonus=float(value_ts_bonus),
            ffs_VolumeWeightIsOver=float(value_ffs_VolumeWeightIsOver),
            ffs_TasteRatingIsOver=float(value_ffs_TasteRatingIsOver),
            ffs_BrownIntactRatioIsOver=float(value_ffs_BrownIntactRatioIsOver),
            tgap_bonus=float(value_tgap_bonus),
            final_PrimeYieldIsOverAndEqualTo=float(
                value_final_PrimeYieldIsOverAndEqualTo),
            multiplication=float(value_multiplication),
            maxPurchaseQTYPerHectare=float(value_maxPurchaseQTYPerHectare),
            blackCat_customer_id=value_blackCat_customer_id,
            blackCat_api_token=value_blackCat_api_token,
            blackCat_api_url=value_blackCat_api_url,
            ecan_customer_id=value_ecan_customer_id,
            ktj_customer_id=value_ktj_customer_id,
        )
        return res
