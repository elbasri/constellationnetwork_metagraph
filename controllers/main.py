from odoo import http
from odoo.http import request
import logging
from datetime import datetime
from werkzeug.utils import redirect

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
        transaction_hash = post.get('dag_transaction_hash')
        reference = post.get('reference')
        _logger.info('Transaction hash: %s, Reference: %s', transaction_hash, reference)

        # Strip or adjust the reference if necessary
        stripped_reference = reference.split('-')[0]

        # Find the payment transaction
        tx = request.env['payment.transaction'].sudo().search([('reference', '=', reference)])
        if not tx:
            _logger.error('Transaction not found for reference %s', reference)
            return request.redirect('/payment/process')
        _logger.info('Found transaction: %s', tx)

        # Attempt to link with Sale Order or Invoice
        sale_order = request.env['sale.order'].sudo().search([('name', '=', stripped_reference)], limit=1)
        invoice = request.env['account.move'].sudo().search([('payment_reference', '=', stripped_reference), ('move_type', '=', 'out_invoice')], limit=1)
        
        # If the stripped reference doesn't work, try original reference as fallback
        if not sale_order:
            sale_order = request.env['sale.order'].sudo().search([('name', '=', reference)], limit=1)
        if not invoice:
            invoice = request.env['account.move'].sudo().search([('payment_reference', '=', reference), ('move_type', '=', 'out_invoice')], limit=1)

        _logger.info('Found sale order: %s', sale_order)
        _logger.info('Found invoice: %s', invoice)

        request.env.cr.autocommit(False)  # Disable autocommit
        try:
            metagraph = request.env['metagraph'].sudo().search([('transaction_hash', '=', transaction_hash)], limit=1)
            if not metagraph:
                metagraph_data = {
                    'name': f'Transaction {transaction_hash}',
                    'metagraph_details': f'Details for transaction {transaction_hash}',
                    'transaction_hash': transaction_hash,
                    'blockchain_status': 'pending',
                    'wallet_address_id': request.env['metagraph.config'].sudo().search([], limit=1).id,
                    'created_date': datetime.now(),
                    'amount': float(post.get('amount', 0)),
                    'source': post.get('dag_wallet_address'),
                    'destination': tx.acquirer_id.dag_wallet_address,
                    'fee': 0,
                    'parent_hash': '',
                    'parent_ordinal': 0,
                    'block_hash': '',
                    'snapshot_hash': '',
                    'snapshot_ordinal': 0,
                    'timestamp': datetime.now(),
                    'salt': '',
                    'proof_id': '',
                    'proof_signature': '',
                    'sale_order_id': sale_order.id if sale_order else None,
                    'invoice_id': invoice.id if invoice else None,
                }
                _logger.info('Creating new Metagraph record with data: %s', metagraph_data)
                metagraph = request.env['metagraph'].create(metagraph_data)
                _logger.info('Metagraph record created successfully: %s', metagraph)
            else:
                # If the metagraph exists, update either the Sale Order ID or the Invoice ID
                if sale_order:
                    _logger.info('Linking existing Metagraph record to Sale Order ID: %s', sale_order.id)
                    metagraph.write({'sale_order_id': sale_order.id})
                elif invoice:
                    _logger.info('Linking existing Metagraph record to Invoice ID: %s', invoice.id)
                    metagraph.write({'invoice_id': invoice.id})
                _logger.info('Metagraph record updated successfully: %s', metagraph)

            _logger.info('Checking status of Metagraph transaction: %s', transaction_hash)
            metagraph.check_status()
            if metagraph.blockchain_status == 'confirmed':
                tx._set_transaction_done()
                _logger.info('Transaction confirmed. Marking as done and updating Metagraph.')
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
                request.env.cr.commit()
                _logger.info('Database transaction committed successfully.')
                return redirect('/payment/process')
            else:
                tx._set_transaction_cancel()
                request.env.cr.rollback()
                _logger.info('Transaction not confirmed, rolling back.')
                return redirect('/payment/process') 
        except Exception as e:
            tx._set_transaction_cancel()
            request.env.cr.rollback()
            _logger.exception('An error occurred, and the transaction was rolled back: %s', str(e))
            return request.redirect('/payment/process')
        finally:
            request.env.cr.autocommit(True)
