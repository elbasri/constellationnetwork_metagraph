{
    'name': 'Metagraph Management',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Manage Constellation Network Metagraph',
    'description': """
        Module to manage metagraphs and their configurations for Constellation Network
    """,
    'author': 'ABDENNACER Elbasri',
    'depends': ['base', 'mail', 'sale', 'stock', 'payment'],
    'data': [
        'views/metagraph_views.xml',
        'security/ir.model.access.csv',
        'views/metagraph_config_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/payment_template_dag.xml',
        'views/payment_acquirer_dag_views.xml',
        'data/payment_acquirer_dag_data.xml',
    ],
    'installable': True,
    'application': True,
}
