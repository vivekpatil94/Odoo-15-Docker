from requests import request
from odoo import http
import json


class Dolimi(http.Controller):

    @http.route('/api/v1/agriculture/crops', type='http', auth="public", methods=['GET'], csrf=False)
    def crops(self):
        crops = http.request.env['agriculture.crop'].sudo().search([])
        data = []
        for record in crops:
            data.append({
                'SeqNumber': record.SeqNumber,
                'FarmerType': record.SellerName.FarmerType,
                'LastCreationTime': record.LastCreationTime,
            })
            # data.append({
            #     'SeqNumber': record.SeqNumber,
            #     'SellerName': record.SellerName.SellerName,
            #     'SellerId': record.SellerName.SellerId,
            #     'Region': record.SellerName.Region,
            #     'AuxId': record.SellerName.AuxId,
            #     'FarmerType': record.SellerName.FarmerType,
            #     'FarmingMethod': record.FarmingMethod,
            #     'CropVariety': record.CropVariety.CropVariety_name,
            #     'CropVariety_bonus': record.CropVariety.CropVariety_bonus,
            #     'CropStatus': record.CropStatus,
            #     'CropType': record.CropType,
            #     'isTGAP': record.isTGAP,
            #     'FarmingAdaption': record.FarmingAdaption,
            #     'BrownYield': record.BrownYield,
            #     'HullYield': record.HullYield,
            #     'BranYield': record.BranYield,
            #     'PrimeYield': record.PrimeYield,
            #     'BBRiceYield': record.BBRiceYield,
            #     'SBRiceYield': record.SBRiceYield,
            #     'RawHumidity': record.RawHumidity,
            #     'BrownHumidity': record.BrownHumidity,
            #     'RiceHumidity': record.RiceHumidity,
            #     'BrownIntactRatio': record.BrownIntactRatio,
            #     'BrownCrackedRatio': record.BrownCrackedRatio,
            #     'BrownImmatureRatio': record.BrownImmatureRatio,
            #     'BrownPestsRatio': record.BrownPestsRatio,
            #     'BrownColoredRatio': record.BrownColoredRatio,
            #     'BrownDeadRatio': record.BrownDeadRatio,
            #     'TasteRating': record.TasteRating,
            #     'Protein': record.Protein,
            #     'BrownMoisture': record.BrownMoisture,
            #     'BrownAmylose': record.BrownAmylose,
            #     'VolumeWeight': record.VolumeWeight,
            #     'CarCropWeight': record.CarCropWeight,
            #     'CarWeight': record.CarWeight,
            #     'HarvestYear': record.HarvestYear,
            #     'HarvestPeriod': record.HarvestPeriod,
            #     'LastCreationTime': record.LastCreationTime,
            #     'CropWeight': record.CropWeight,
            #     'StorageId': record.StorageId,
            #     'DryerId': record.DryerId,
            #     'StartTime': record.StartTime,
            #     'EndTime': record.EndTime,
            #     'stage_id': record.stage_id.state,
            #     'FinalPrice': record.FinalPrice,
            #     'TotalPrice': record.TotalPrice,
            # })

        # return json.dumps(data, default=str)
        return http.Response(
            json.dumps(data, default=str),
            status=200,
            mimetype='application/json'
        )

    @http.route("/api/v1/test/http", auth='none', type='http', method=['GET'])
    def check_method_get(self, **kwargs):
        output = {
            'results': {
                'code': 200,
                'message': 'OK'
            }
        }
        return json.dumps(output)


# -*- coding: utf-8 -*-
# from odoo import http


# class Dolimi(http.Controller):
#     @http.route('/dolimi/dolimi', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dolimi/dolimi/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dolimi.listing', {
#             'root': '/dolimi/dolimi',
#             'objects': http.request.env['dolimi.dolimi'].search([]),
#         })

#     @http.route('/dolimi/dolimi/objects/<model("dolimi.dolimi"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dolimi.object', {
#             'object': obj
#         })
