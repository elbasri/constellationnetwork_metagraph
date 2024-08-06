from odoo import http, fields, models
from odoo.http import request

class CustomerPortal(http.Controller):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        # Include additional data preparation here if necessary
        return values

    @http.route(['/my/orders/<int:order_id>'], type='http', auth='public', website=True)
    def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        order = request.env['sale.order'].sudo().browse(order_id)
        metagraphs = request.env['metagraph'].sudo().search([('sale_order_id', '=', order.id)])
        values = {
            'order': order,
            'metagraphs': metagraphs,
        }
        return request.render("constellationnetwork_metagraph.portal_order_metagraph", values)

    @http.route(['/my/invoices/<int:invoice_id>'], type='http', auth='public', website=True)
    def portal_invoice_page(self, invoice_id, report_type=None, access_token=None, message=False, download=False, **kw):
        invoice = request.env['account.move'].sudo().browse(invoice_id)
        metagraphs = request.env['metagraph'].sudo().search([('invoice_id', '=', invoice.id)])
        values = {
            'invoice': invoice,
            'metagraphs': metagraphs,
        }
        return request.render("constellationnetwork_metagraph.portal_invoice_metagraph", values)
