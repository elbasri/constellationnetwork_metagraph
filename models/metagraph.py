from odoo import models, fields, api, exceptions
from .constellation_api import ConstellationAPI
import logging
from datetime import datetime
import time

_logger = logging.getLogger(__name__)

class Metagraph(models.Model):
    _name = 'metagraph'
    _description = 'Metagraph'

    name = fields.Char(string='Metagraph Name', required=True)
    metagraph_details = fields.Text(string='Metagraph Details')
    blockchain_status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed')
    ], string='Blockchain Status', default='pending')
    blockchain_hash = fields.Char(string='Blockchain Hash')
    created_date = fields.Datetime(string='Created Date', default=fields.Datetime.now)
    metagraph_address = fields.Char(string='Metagraph Address')
    transaction_hash = fields.Char(string='Transaction Hash')
    wallet_address_id = fields.Many2one('metagraph.config', string='Wallet Address', required=True)
    environment = fields.Selection(related='wallet_address_id.environment', readonly=True, store=True)
    amount = fields.Float(string='Amount')
    source = fields.Char(string='Source')
    destination = fields.Char(string='Destination')
    fee = fields.Float(string='Fee')
    parent_hash = fields.Char(string='Parent Hash')
    parent_ordinal = fields.Integer(string='Parent Ordinal')
    block_hash = fields.Char(string='Block Hash')
    snapshot_hash = fields.Char(string='Snapshot Hash')
    snapshot_ordinal = fields.Integer(string='Snapshot Ordinal')
    timestamp = fields.Datetime(string='Timestamp')
    salt = fields.Char(string='Salt')
    proof_id = fields.Char(string='Proof ID')
    proof_signature = fields.Char(string='Proof Signature')

    def retry_operation(self, operation, *args, **kwargs):
        max_retries = 5
        for attempt in range(max_retries):
            try:
                return operation(*args, **kwargs)
            except exceptions.UserError as e:
                if 'could not serialize access due to concurrent update' in str(e):
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        raise
                else:
                    raise
            except Exception as e:
                raise

    def check_status(self):
        _logger.info(f"Checking status for transaction hash: {self.transaction_hash}")
        api = ConstellationAPI(self._get_base_url(), self._get_faucet_url(), self._get_check_status_url())
        status = self.retry_operation(api.get_metagraph_status, self.transaction_hash)
        _logger.info(f"Status result: {status}")

        if 'data' in status:
            data = status['data']
            self.blockchain_status = 'confirmed'
            self.blockchain_hash = data.get('hash')
            self.metagraph_address = data.get('destination')
            self.amount = data.get('amount')
            self.source = data.get('source')
            self.destination = data.get('destination')
            self.fee = data.get('fee')
            self.parent_hash = data['parent'].get('hash')
            self.parent_ordinal = data['parent'].get('ordinal')
            self.block_hash = data.get('blockHash')
            self.snapshot_hash = data.get('snapshotHash')
            self.snapshot_ordinal = data.get('snapshotOrdinal')
            self.timestamp = datetime.strptime(data.get('timestamp'), '%Y-%m-%dT%H:%M:%S.%fZ')
            self.salt = data['transactionOriginal']['value'].get('salt')
            self.proof_id = data['transactionOriginal']['proofs'][0].get('id')
            self.proof_signature = data['transactionOriginal']['proofs'][0].get('signature')
        else:
            self.blockchain_status = 'failed'
        
        self.env['bus.bus'].sendone((self._cr.dbname, 'res.partner', self.env.user.partner_id.id), {
            'type': 'simple_notification',
            'title': 'Transaction Status',
            'message': f'Transaction status: {self.blockchain_status}',
            'sticky': False,
        })

    def get_testnet_dag(self):
        _logger.info(f"Requesting TestNet DAG for wallet address: {self.wallet_address_id.wallet_address}")
        api = ConstellationAPI(self._get_base_url(), self._get_faucet_url(), self._get_check_status_url())
        result = self.retry_operation(api.get_testnet_dag, self.wallet_address_id.wallet_address)
        _logger.info(f"TestNet DAG Request Result: {result}")

        if 'data' in result and 'transaction_hash' in result['data']:
            transaction_hash = result['data']['transaction_hash']
            self.transaction_hash = transaction_hash
            self.env['bus.bus'].sendone((self._cr.dbname, 'res.partner', self.env.user.partner_id.id), {
                'type': 'simple_notification',
                'title': 'Success',
                'message': f'TestNet DAG requested successfully. Transaction hash: {transaction_hash}',
                'sticky': False,
            })
        else:
            self.env['bus.bus'].sendone((self._cr.dbname, 'res.partner', self.env.user.partner_id.id), {
                'type': 'simple_notification',
                'title': 'Warning',
                'message': 'Failed to request TestNet DAG. Please try again later.',
                'sticky': False,
            })

    def _get_base_url(self):
        if self.environment == 'testnet':
            return self.wallet_address_id.testnet_url
        elif self.environment == 'integration':
            return self.wallet_address_id.integration_url
        return self.wallet_address_id.mainnet_url

    def _get_faucet_url(self):
        if self.environment == 'testnet':
            return self.wallet_address_id.faucet_testnet_url
        elif self.environment == 'integration':
            return self.wallet_address_id.faucet_integration_url
        return self.wallet_address_id.faucet_mainnet_url

    def _get_check_status_url(self):
        if self.environment == 'testnet':
            return self.wallet_address_id.check_status_testnet_url
        elif self.environment == 'integration':
            return self.wallet_address_id.check_status_integration_url
        return self.wallet_address_id.check_status_mainnet_url
