from odoo import models, fields

class MetagraphReport(models.Model):
    _name = 'metagraph.report'
    _description = 'Metagraph Report'
    _auto = False  # This model will not create a table in the database

    name = fields.Char(string='Metagraph Name')
    amount = fields.Float(string='Amount')
    blockchain_status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed')
    ], string='Blockchain Status')
    timestamp = fields.Datetime(string='Timestamp')

    def init(self):
        """ This method will be called when the module is installed/upgraded.
            It creates the SQL view that is used to aggregate data for reporting.
        """
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW metagraph_report AS (
                SELECT
                    row_number() OVER () AS id,
                    name,
                    amount,
                    blockchain_status,
                    timestamp
                FROM
                    metagraph
            )
        """)
