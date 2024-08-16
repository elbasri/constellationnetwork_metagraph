from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    metagraph_ids = fields.One2many(
        'metagraph', 'sale_order_id', string='DAG Transactions'
    )

    def action_confirm(self):
        super(SaleOrder, self).action_confirm()
        for metagraph in self.metagraph_ids:
            metagraph.check_status()

    def action_done(self):
        res = super(SaleOrder, self).action_done()
        for metagraph in self.metagraph_ids:
            metagraph.check_status()
        return res
