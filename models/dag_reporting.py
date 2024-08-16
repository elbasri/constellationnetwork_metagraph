from odoo import models, fields, api

class DAGTransactionReport(models.Model):
    _name = 'dag.transaction.report'
    _description = 'DAG Transaction Report'

    name = fields.Char(string='Report Name', required=True)
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    transaction_ids = fields.Many2many('metagraph', string='Transactions')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount')
    total_fee = fields.Float(string='Total Fee', compute='_compute_total_fee')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string='Status', default='draft')

    @api.depends('transaction_ids')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(transaction.amount for transaction in record.transaction_ids)

    @api.depends('transaction_ids')
    def _compute_total_fee(self):
        for record in self:
            record.total_fee = sum(transaction.fee for transaction in record.transaction_ids)

    def confirm_report(self):
        self.state = 'confirmed'

class DAGTransactionWizard(models.TransientModel):
    _name = 'dag.transaction.wizard'
    _description = 'DAG Transaction Wizard'

    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)

    def generate_report(self):
        transactions = self.env['metagraph'].search([
            ('timestamp', '>=', self.date_from),
            ('timestamp', '<=', self.date_to)
        ])
        report = self.env['dag.transaction.report'].create({
            'name': f'DAG Transaction Report ({self.date_from} to {self.date_to})',
            'date_from': self.date_from,
            'date_to': self.date_to,
            'transaction_ids': [(6, 0, transactions.ids)],
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'DAG Transaction Report',
            'view_mode': 'form',
            'res_model': 'dag.transaction.report',
            'res_id': report.id,
            'target': 'new',
        }
