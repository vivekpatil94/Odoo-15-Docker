from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class BlackcatObt(models.Model):
    _name = 'agriculture.blackcat_obt'
    _description = 'Blackcat OBT'

    StockPickingId = fields.Many2one('stock.picking')
    SrvTranId = fields.Char('SrvTranId', require=True)
    OBTNumber = fields.Char('OBTNumber', require=True)
    FileNo = fields.Char('FileNo', require=True)
    ShippingPdf = fields.Binary('ShippingPdf')
    ShippingPdfFilename = fields.Char(
        string='PDF Filename',
        compute='_compute_pdf_filename'
    )

    @api.depends('ShippingPdf')
    def _compute_pdf_filename(self):
        self.ensure_one()
        name = self.OBTNumber.replace('/', '_')
        name = name.replace('.', '_')
        name = name + '.pdf'
        self.ShippingPdfFilename = name

    def name_get(self):
        result = []
        for record in self:
            record_name = 'Id: {id} 單號: {obt}'.format(
                id=record.id, obt=record.OBTNumber)
            result.append((record.id, record_name))
        return result
