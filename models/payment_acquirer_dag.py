from odoo import models, fields, api, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
import urllib.parse

class PaymentAcquirerDAG(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('dag', 'DAG')], ondelete={'dag': 'set default'})
    dag_wallet_address = fields.Char(string='DAG Wallet Address', compute='_compute_dag_wallet_address', store=False)

    @api.depends('provider')
    def _compute_dag_wallet_address(self):
        config = self.env['metagraph.config'].search([], limit=1)
        for record in self:
            if config:
                record.dag_wallet_address = config.wallet_address

    def dag_get_form_action_url(self):
        return '/payment/dag/form'

    def dag_form_generate_values(self, values):
        config = self.env['metagraph.config'].search([], limit=1)
        if not config:
            raise ValidationError(_('DAG configuration is missing.'))

        base_url = self.get_base_url()
        dag_tx_values = dict(values)
        dag_tx_values.update({
            'wallet_address': config.wallet_address,
            'callback_url': '%s' % urllib.parse.urljoin(base_url, 'payment/dag/feedback'),
            'return_url': '%s' % urllib.parse.urljoin(base_url, 'payment/process'),
        })
        return dag_tx_values

class PaymentTransactionDAG(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _dag_form_get_tx_from_data(self, data):
        reference = data.get('reference')
        if not reference:
            raise ValidationError(_('DAG: received data with missing reference'))
        tx = self.search([('reference', '=', reference)])
        if not tx or len(tx) > 1:
            error_msg = _('DAG: received data for reference %s') % (reference)
            if not tx:
                error_msg += _('; no order found')
            else:
                error_msg += _('; multiple orders found')
            raise ValidationError(error_msg)
        return tx

    def _dag_form_validate(self, data):
        status = data.get('status')
        if status == 'confirmed':
            self._set_transaction_done()
            return True
        elif status == 'pending':
            self._set_transaction_pending()
            return True
        else:
            self._set_transaction_cancel()
            return False
