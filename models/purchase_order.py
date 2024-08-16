from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    metagraph_ids = fields.One2many(
        'metagraph', 'purchase_order_id', string='DAG Transactions'
    )

    def button_confirm(self):
        super(PurchaseOrder, self).button_confirm()
        for metagraph in self.metagraph_ids:
            metagraph.check_status()

    def button_approve(self, force=False):
        res = super(PurchaseOrder, self).button_approve(force)
        for metagraph in self.metagraph_ids:
            metagraph.check_status()
        return res
