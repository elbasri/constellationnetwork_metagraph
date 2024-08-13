{
    'name': 'Metagraph Management',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Manage Constellation Network Metagraph',
    'description': """
        Module to manage metagraphs and their configurations for Constellation Network
    """,
    'author': 'ABDENNACER Elbasri',
    'depends': ['base', 'mail', 'sale', 'stock', 'payment', 'website', 'account'],
    'data': [
        'views/metagraph_views.xml',
        'security/ir.model.access.csv',
        'views/metagraph_config_views.xml',
        'views/stock_picking_views.xml',
        'views/payment_template_dag.xml',
        'views/payment_acquirer_dag_views.xml',
        'data/payment_acquirer_dag_data.xml',
        'views/account_move_view.xml',
        'views/sale_order_views.xml',
        'views/payment_dag_thank_you_page.xml',
        'views/payment_dag_error_page.xml',
        #'templates/portal_invoice_metagraph.xml',
        #'templates/portal_order_metagraph.xml',
        'views/report_invoice_with_dag.xml',
        
    ],
    'installable': True,
    'application': True,
    'controllers': ['controllers/main.py'],
}
