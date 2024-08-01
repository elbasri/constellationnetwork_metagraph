from odoo import http
from odoo.http import request
import logging

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
        
        # Locate the metagraph record using transaction hash
        metagraph = request.env['metagraph'].sudo().search([('transaction_hash', '=', transaction_hash)], limit=1)
        if not metagraph:
            _logger.error('Metagraph record not found for transaction hash %s', transaction_hash)
            return request.redirect('/payment/process')

        # Call check_status method on the located metagraph record
        _logger.error('Call check_status method')
        metagraph.check_status()
        if metagraph.blockchain_status == 'confirmed':
            _logger.error('Call check_status method confirmed')
            tx._set_transaction_done()
            _logger.error('Call check_status method _set_transaction_done')
            return request.render('constellationnetwork_metagraph.payment_dag_thank_you_page', {})
        else:
            _logger.error('Call check_status method not confirmed')
            tx._set_transaction_cancel()
            _logger.error('Call check_status method not confirmed _set_transaction_cancel')
            return request.render('constellationnetwork_metagraph.payment_dag_error_page', {})
