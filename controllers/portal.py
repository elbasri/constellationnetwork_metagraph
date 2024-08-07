from odoo import http
from odoo.http import request

class CustomerPortal(http.Controller):
    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        # Include additional data preparation here if necessary
        return values

    @http.route(['/my/orders/<int:order_id>'], type='http', auth='user', website=True)
    def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        sale_order = request.env['sale.order'].sudo().browse(order_id)
        if not sale_order.exists():
            return request.redirect('/my')  # Redirect if the order does not exist

        values = {
            'sale_order': sale_order,
            'metagraphs': sale_order.metagraph_ids,
            'report_type': report_type,
            'access_token': access_token,
            'message': message,
            'download': download,
        }
        return request.render("constellationnetwork_metagraph.portal_order_metagraph", values)

    @http.route(['/my/invoices/<int:invoice_id>'], type='http', auth='user', website=True)
    def portal_invoice_page(self, invoice_id, report_type=None, access_token=None, message=False, download=False, **kw):
        invoice = request.env['account.move'].sudo().browse(invoice_id)
        if not invoice.exists():
            return request.redirect('/my')  # Redirect if the invoice does not exist

        values = {
            'invoice': invoice,
            'metagraphs': invoice.metagraph_ids,
            'report_type': report_type,
            'access_token': access_token,
            'message': message,
            'download': download,
        }
        return request.render("constellationnetwork_metagraph.portal_invoice_metagraph", values)
