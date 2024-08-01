from odoo import http
from odoo.http import request
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class PaymentDagController(http.Controller):

    @http.route(['/payment/dag/form'], type='http', auth='public', website=True)
    def dag_payment_form(self, **kwargs):
        _logger.info('Received kwargs for /payment/dag/form: %s', kwargs)
        acquirer = request.env['payment.acquirer'].sudo().search([('provider', '=', 'dag')], limit=1)
        values = {
            'acquirer': acquirer,
            'reference': kwargs.get('reference'),
            'amount': kwargs.get('amount'),
            'currency_id': kwargs.get('currency_id'),
            'partner_id': kwargs.get('partner_id'),
            'order_id': kwargs.get('order_id'),
            'company_id': kwargs.get('company_id'),
            'access_token': kwargs.get('access_token'),
        }
        _logger.info('Values prepared for rendering: %s', values)
        return request.render('constellationnetwork_metagraph.payment_dag_form', values)

    @http.route(['/payment/dag/feedback'], type='http', auth='public', methods=['POST'], csrf=False)
    def dag_feedback(self, **post):
        _logger.info('DAG payment feedback received with post data: %s', post)

        # Extract transaction hash and reference
        transaction_hash = post.get('dag_transaction_hash')
        reference = post.get('reference')
        
        # Validate transaction
        tx = request.env['payment.transaction'].sudo().search([('reference', '=', reference)])
        if not tx:
            _logger.error('Transaction not found for reference %s', reference)
            return request.redirect('/payment/process')
        
        # Locate or create the metagraph record using transaction hash
        metagraph = request.env['metagraph'].sudo().search([('transaction_hash', '=', transaction_hash)], limit=1)
        if not metagraph:
            _logger.info('Creating new Metagraph record for transaction hash %s', transaction_hash)
            metagraph = request.env['metagraph'].create({
                'name': 'Transaction ' + transaction_hash,
                'metagraph_details': 'Details for transaction ' + transaction_hash,
                'transaction_hash': transaction_hash,
                'blockchain_status': 'pending',  # Initial status, will be updated after check_status
                'wallet_address_id': request.env['metagraph.config'].sudo().search([], limit=1).id,
                'created_date': datetime.now(),
                'amount': float(post.get('amount', 0)),
                'source': post.get('source_address'),
                'destination': post.get('destination_address'),
                'fee': float(post.get('fee', 0)),
                'parent_hash': post.get('parent_hash'),
                'parent_ordinal': int(post.get('parent_ordinal', 0)),
                'block_hash': post.get('block_hash'),
                'snapshot_hash': post.get('snapshot_hash'),
                'snapshot_ordinal': int(post.get('snapshot_ordinal', 0)),
                'timestamp': datetime.now(),
                'salt': post.get('salt'),
                'proof_id': post.get('proof_id'),
                'proof_signature': post.get('proof_signature'),
            })

        # Call check_status method on the located or newly created metagraph record
        metagraph.check_status()
        if metagraph.blockchain_status == 'confirmed':
            _logger.info('Transaction confirmed for transaction hash %s', transaction_hash)
            tx._set_transaction_done()
            # Update existing metagraph record to confirmed
            metagraph.write({
                'blockchain_status': 'confirmed',
                'blockchain_hash': metagraph.blockchain_hash,
                'metagraph_address': metagraph.metagraph_address,
                'amount': metagraph.amount,
                'source': metagraph.source,
                'destination': metagraph.destination,
                'fee': metagraph.fee,
                'parent_hash': metagraph.parent_hash,
                'parent_ordinal': metagraph.parent_ordinal,
                'block_hash': metagraph.block_hash,
                'snapshot_hash': metagraph.snapshot_hash,
                'snapshot_ordinal': metagraph.snapshot_ordinal,
                'timestamp': metagraph.timestamp,
                'salt': metagraph.salt,
                'proof_id': metagraph.proof_id,
                'proof_signature': metagraph.proof_signature,
            })
            return request.render('constellationnetwork_metagraph.payment_dag_thank_you_page', {})
        else:
            _logger.info('Transaction not confirmed for transaction hash %s', transaction_hash)
            tx._set_transaction_cancel()
            return request.render('constellationnetwork_metagraph.payment_dag_error_page', {})
