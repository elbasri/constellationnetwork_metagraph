from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    transaction_hash = fields.Char(string='Transaction Hash')
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], string='Payment Status', default='pending')

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        if self.payment_status == 'completed':
            _logger.info(f"Stock Picking {self.name} validated with payment status: {self.payment_status}")
        else:
            _logger.warning(f"Stock Picking {self.name} has not been completed. Payment status: {self.payment_status}")
        return res
