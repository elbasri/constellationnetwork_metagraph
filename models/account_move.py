from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    metagraph_ids = fields.One2many(
        'metagraph', 'invoice_id', string='DAG Transactions'
    )
