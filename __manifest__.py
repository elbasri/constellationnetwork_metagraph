{
    'name': 'Metagraph Management',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Manage Constellation Network Metagraph',
    'description': """
        Module to manage metagraphs and their configurations for Constellation Network
    """,
    'images': ['static/description/icon.png'],
    'web_icon_data': '/your_module/static/description/icon.png',
    'author': 'ABDENNACER Elbasri',
    'depends': ['base', 'sale', 'stock', 'payment', 'website', 'account', 'purchase'],
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
        'views/report_invoice_with_dag.xml',
        'views/report_saleorder_with_dag.xml',
        'views/purchase_order_view.xml',
        'views/dag_transaction_report_views.xml',
        'views/metagraph_report_views.xml',
    ],
    'assets': {
       'web.assets_backend': [
           'your_module/static/description/icon.png',
       ],
    },
    'installable': True,
    'application': True,
    'controllers': ['controllers/main.py'],
}
