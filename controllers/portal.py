from odoo import http
from odoo.http import request

class CustomerPortal(http.Controller):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        # Include additional data preparation here if necessary
        return values

    @http.route(['/my/ordersold/<int:order_id>'], type='http', auth='user', website=True)
    def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        # Ensure that the user has access to this order
        sale_order = request.env['sale.order'].sudo().browse(order_id)
        if not sale_order or sale_order.partner_id != request.env.user.partner_id:
            return request.redirect('/my')  # Redirect to the user's portal if access is denied

        # Prepare the data for rendering the template
        values = {
            'sale_order': sale_order,
            'metagraphs': sale_order.metagraph_ids,
            'report_type': report_type,
            'access_token': access_token,
            'message': message,
            'download': download,
        }
        return request.render("constellationnetwork_metagraph.portal_order_metagraph", values)

    @http.route(['/my/invoicesold/<int:invoice_id>'], type='http', auth='user', website=True)
    def portal_invoice_page(self, invoice_id, report_type=None, access_token=None, message=False, download=False, **kw):
        # Ensure that the user has access to this invoice
        invoice = request.env['account.move'].sudo().browse(invoice_id)
        if not invoice or invoice.partner_id != request.env.user.partner_id:
            return request.redirect('/my')  # Redirect to the user's portal if access is denied

        # Prepare the data for rendering the template
        values = {
            'invoice': invoice,
            'metagraphs': invoice.metagraph_ids,
            'report_type': report_type,
            'access_token': access_token,
            'message': message,
            'download': download,
        }
        return request.render("constellationnetwork_metagraph.portal_invoice_metagraph", values)
