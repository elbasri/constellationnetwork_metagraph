from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    metagraph_ids = fields.One2many(
        'metagraph', 'picking_id', string='DAG Transactions'
    )

    def action_confirm(self):
        super(StockPicking, self).action_confirm()
        for metagraph in self.metagraph_ids:
            metagraph.check_status()

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for metagraph in self.metagraph_ids:
            metagraph.check_status()
        return res
