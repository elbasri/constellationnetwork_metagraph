from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class PaymentDagController(http.Controller):

    @http.route(['/payment/dag/form'], type='http', auth='public', website=True)
    def dag_payment_form(self, **kwargs):
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
        
        # Call check_status function
        metagraph = request.env['metagraph.config'].sudo().search([], limit=1)
        if not metagraph:
            _logger.error('Metagraph configuration not found')
            return request.redirect('/payment/process')

        status = metagraph.check_status(transaction_hash)
        if status == 'confirmed':
            tx._set_transaction_done()
            return request.render('constellationnetwork_metagraph.payment_dag_thank_you_page', {})
        else:
            tx._set_transaction_cancel()
            return request.render('constellationnetwork_metagraph.payment_dag_error_page', {})
