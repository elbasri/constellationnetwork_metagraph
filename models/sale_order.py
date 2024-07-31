from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    transaction_hash = fields.Char(string='Transaction Hash')
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], string='Payment Status', default='pending')

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            _logger.info(f"Sale Order {order.name} confirmed with payment status: {order.payment_status}")
        return res
