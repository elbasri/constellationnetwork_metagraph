from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    metagraph_ids = fields.One2many(
        'metagraph', 'sale_order_id', string='DAG Transactions'
    )
