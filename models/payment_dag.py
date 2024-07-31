from odoo import models, fields, api
import logging
from .constellation_api import ConstellationAPI

_logger = logging.getLogger(__name__)

class PaymentDag(models.Model):
    _name = 'payment.dag'
    _description = 'DAG Payment'

    name = fields.Char(string='Payment Reference', required=True)
    source_wallet = fields.Char(string='Source Wallet', required=True)
    destination_wallet = fields.Char(string='Destination Wallet', required=True)
    amount = fields.Float(string='Amount', required=True)
    fee = fields.Float(string='Fee', default=0)
    transaction_hash = fields.Char(string='Transaction Hash')
    status = fields.Selection([
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], string='Status', default='pending')
    metagraph_config_id = fields.Many2one('metagraph.config', string='Metagraph Config', required=True)

    def send_payment(self):
        _logger.info(f"Sending payment from {self.source_wallet} to {self.destination_wallet}")
        api = ConstellationAPI(
            self.metagraph_config_id.base_url,
            self.metagraph_config_id.faucet_url,
            self.metagraph_config_id.check_status_url,
            self.metagraph_config_id.payment_url
        )
        result = api.send_payment(
            self.source_wallet, 
            self.destination_wallet, 
            self.amount, 
            self.fee
        )
        _logger.info(f"Payment result: {result}")

        if 'transaction_hash' in result:
            self.transaction_hash = result['transaction_hash']
            self.status = 'completed'
        else:
            self.status = 'failed'

        self.env['bus.bus'].sendone((
            self._cr.dbname, 'res.partner', self.env.user.partner_id.id), {
            'type': 'simple_notification',
            'title': 'Payment Status',
            'message': f'Payment status: {self.status}',
            'sticky': False,
        })
