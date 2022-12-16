from odoo import models, fields, api, exceptions
from odoo.tools.translate import _
from datetime import timedelta, date
import logging
from .blackcatapi import PrintObtOrder, PrintObtRequestData, SearchAddress, AddressRequestData, ShippingPdfRequestData, \
    get_zipcode, request_print_obt, request_address, request_pdf

_logger = logging.getLogger(__name__)


DefinedBlackcatState = [
    ('none', 'None'),
    ('obtRequested', 'OBT Requested'),
    ('printRequested', 'Print Requested'),
]


class Inherit_stock_picking(models.Model):
    _inherit = 'stock.picking'

    BlackcatObtId = fields.Many2one(
        'agriculture.blackcat_obt', compute='compute_blackcat_obt', inverse='blackcat_obt_inverse')
    BlackcatObtIds = fields.One2many(
        'agriculture.blackcat_obt', 'StockPickingId', 'Blackcat OBT')
    BlackcatState = fields.Selection(
        DefinedBlackcatState, 'State', default=DefinedBlackcatState[0][0])

    # '''需新增packageName對應至商品分類項目'''
    # PackageName = fields.Char(
    #     "PackageName", require=True)
    ShipmentDate = fields.Date(
        "ShipmentDate", require=True, default=date.today())
    HopeArriveDate = fields.Date(
        "HopeArriveDate", require=True, default=date.today()+timedelta(days=3))

    Shipping_method = fields.Char('Shipping Method', default='', readonly=True)
    temp_conpany_phone = fields.Char('temp_conpany_phone', default='')

    @api.depends('BlackcatObtIds')
    def compute_blackcat_obt(self):
        idx = len(self.BlackcatObtIds)
        if idx > 0:
            self.BlackcatObtId = self.BlackcatObtIds[idx - 1]

    def blackcat_obt_inverse(self):
        idx = len(self.BlackcatObtIds)
        if idx > 0:
            # delete previous reference
            asset = self.env['agriculture.blackcat_obt'].browse(
                self.BlackcatObtIds[0].id)
            asset.StockPickingId = False
        # set new reference
        self.BlackcatObtId.StockPickingId = self

    def create_notification(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Success'),
                'type': 'success',
                'sticky': False,
                'fadeout': 'slow',
                'next': {
                    'type': 'ir.actions.act_window_close',
                }
            }
        }

    def no_carrier_notification(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('no carrier selected!'),
                'type': 'success',
                'sticky': False,
                'fadeout': 'slow',
                'next': {
                    'type': 'ir.actions.act_window_close',
                }
            }
        }

    def requestBlackCat(self, packageItems):
        # if not self.PackageName:
        #     raise exceptions.ValidationError(
        #         'Package name must not be empty')
        if not self.ShipmentDate:
            raise exceptions.ValidationError(
                'Shipment date must not be empty')
        if not self.HopeArriveDate:
            raise exceptions.ValidationError(
                'HopeArrive date must not be empty')
        # recipientPhone = self.partner_id.Member.get_partner_attr(
        #     'mobile-or-phone').replace('+886', '0').replace(" ", "")
        if self.partner_id.mobile:
            if self.partner_id.mobile.startswith('+886'):
                recipientPhone = self.partner_id.mobile.replace(
                    '+886', '0').replace(" ", "")
            else:
                recipientPhone = self.partner_id.mobile
        else:
            if self.partner_id.phone.startswith('+886'):
                recipientPhone = self.partner_id.phone.replace(
                    '+886', '0').replace(" ", "")
            else:
                recipientPhone = self.partner_id.phone

        if not recipientPhone:
            raise exceptions.ValidationError(
                'Recipient phone must not be empty')
        # recipientAddress = self.partner_id.Member.get_partner_attr('address')
        # recipientAddress = self.partner_id.contact_address
        if self.partner_id.street2:
            recipientAddress = "{0}{1}{2}{3}".format(
                self.partner_id.zip, self.partner_id.city, self.partner_id.street, self.partner_id.street2)
        else:
            recipientAddress = "{0}{1}{2}".format(
                self.partner_id.zip, self.partner_id.city, self.partner_id.street)

        _logger.info('recipientAddress: %s', recipientAddress)

        if not recipientAddress:
            raise exceptions.ValidationError(
                'Recipient address must not be empty')

        current_company = self.env.company
        if not current_company.phone:
            raise exceptions.ValidationError(
                'Company phone must not be empty')
        senderAddress = "{0}{1}".format(
            current_company.city, current_company.street)
        if not senderAddress:
            raise exceptions.ValidationError(
                'Company address must not be empty')

        # _logger.info('order id: {0}'.format(self.origin))
        # _logger.info('customer.name: {0}'.format(self.partner_id.SellerName))
        # _logger.info('customer.phone: {0}'.format(
        #     self.partner_id.Member.get_partner_attr('total-phone')))
        # _logger.info('customer.address: {0}'.format(
        #     self.partner_id.Member.get_partner_attr('address')))
        # _logger.info('==========')

        # _logger.info('customer.name: {0}'.format(current_company.name))
        # _logger.info('customer.phone: {0}'.format(current_company.phone))
        # _logger.info('customer.address: {0}{1}'.format(
        #     current_company.city, current_company.street))
        # _logger.info('==========')
        # _logger.info('product.name: {0}'.format(self.PackageName))
        # _logger.info('shipment date: {0}'.format(
        #     self.ShipmentDate.strftime('%Y%m%d')))
        # _logger.info('delivery date: {0}'.format(
        #     self.HopeArriveDate.strftime('%Y%m%d')))

        # _logger.info('phone: {0}'.format(recipientPhone))
        # _logger.info('company_phone: {0}'.format(
        #     current_company.phone.replace('+886', '0').replace(" ", "")))

        config = self.env['ir.config_parameter'].sudo()
        customerId = config.get_param('agriculture.blackCat_customer_id')
        customerToken = config.get_param('agriculture.blackCat_api_token')
        apiBaseUrl = config.get_param('agriculture.blackCat_api_url')
        if not customerId:
            raise exceptions.ValidationError('請設定黑貓客戶編號')
        if not customerToken:
            raise exceptions.ValidationError('請設定黑貓授權碼')
        if not apiBaseUrl:
            raise exceptions.ValidationError('請設定黑貓 API URL')

        # 預設商品名稱
        products = ''
        for record in self.move_line_ids_without_package:
            products += record.product_id.name + ' '
            _logger.info('product: %s', products)
        productName = products
        note = ''

        searchAddress = SearchAddress(Search=senderAddress)
        addressRequest = AddressRequestData(
            CustomerId=customerId,
            CustomerToken=customerToken,
            Addresses=[searchAddress]
        )

        zipCode = str('')
        addressResponse = request_address(apiBaseUrl, addressRequest)
        if addressResponse['success']:
            # Create black obt
            addressResData = addressResponse['data']
            # _logger.info(addressResData)
            if not addressResData:
                raise exceptions.ValidationError(
                    'Address Response data is null')
            postNumber = addressResData['Data']['Addresses'][0]['PostNumber']
            zipCode = get_zipcode(postNumber=postNumber)
        else:
            raise exceptions.ValidationError(addressResponse['error'])

        if current_company.phone.startswith('+886'):
            self.temp_conpany_phone = current_company.phone.replace(
                '+886', '0').replace(" ", "")

        orderData = PrintObtOrder(
            OrderId=self.origin,
            Thermosphere="0001",
            Spec="0004",
            ReceiptLocation="01",
            # RecipientName=self.partner_id.SellerName,
            RecipientName=self.partner_id.name,
            RecipientTel=recipientPhone,
            RecipientAddress=recipientAddress,
            SenderName=current_company.name,
            SenderTel=self.temp_conpany_phone,
            SenderZipCode=zipCode,
            SenderAddress=senderAddress,
            ShipmentDate=self.ShipmentDate.strftime('%Y%m%d'),
            DeliveryDate=self.HopeArriveDate.strftime('%Y%m%d'),
            DeliveryTime="02",  # TODO
            IsFreight="N",
            IsCollection="N",
            CollectionAmount=0,
            IsSwipe="N",
            IsDeclare="N",
            DeclareAmount=0,
            ProductTypeId="0001",
            ProductName=productName,
            Memo=note
        )
        orderRequest = PrintObtRequestData(
            CustomerId=customerId,
            CustomerToken=customerToken,
            PrintOBTType="01",
            PrintType="01",
            Orders=[orderData])
        orderReponse = request_print_obt(apiBaseUrl, orderRequest)
        # _logger.info(response)
        if orderReponse['success']:
            self.BlackcatState = DefinedBlackcatState[1][0]
            # Create black obt
            data = orderReponse['data']
            # _logger.info(data)
            if not data:
                raise exceptions.ValidationError(
                    'Print Obt Response data is null')

            pdfRequestData = ShippingPdfRequestData(
                CustomerId=customerId,
                CustomerToken=customerToken,
                FileNo=data['Data']['FileNo']
            )
            binaryData = request_pdf(apiBaseUrl, pdfRequestData)

            self.write({'BlackcatObtIds': [
                (0, 0, {
                    'SrvTranId': data['SrvTranId'],
                    'OBTNumber': data['Data']['Orders'][0]['OBTNumber'],
                    'FileNo': pdfRequestData.FileNo,
                    'ShippingPdf': binaryData,
                    'StockPickingId': self
                })
            ]})
            self.BlackcatState = DefinedBlackcatState[2][0]

            return True
        else:
            raise exceptions.ValidationError(orderReponse['error'])

    def requestECan(self, packageItems):

        pass

    def button_carrier_call(self):
        self.ensure_one()
        # 確認為物流貨運公司
        if self.carrier_id:
            if self.carrier_id.name == 'blackcat' or '黑貓宅急便':
                # 呼叫物流貨運公司
                if self.requestBlackCat(self.move_ids_without_package):
                    return self.create_notification()
            if self.carrier_id.name == 'e-can' or '宅配通':
                # 呼叫物流貨運公司
                if self.requestECan(self.move_ids_without_package):
                    return self.create_notification()
        else:
            return self.no_carrier_notification()
        return True

    @api.onchange('carrier_id')
    def _onchange_(self):
        for rec in self:
            rec.Shipping_method = self.carrier_id.name
            _logger.info(f"carrier_id name: {rec.Shipping_method}")

    @api.model
    def create(self, vals):
        self.env.cr.commit()
        return super(Inherit_stock_picking, self).create(vals)
