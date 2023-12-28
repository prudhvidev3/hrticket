# -*- coding: utf-8 -*-
from odoo import http
import requests  # Import the requests library
from odoo.http import request
from werkzeug.utils import redirect
from odoo.addons.portal.controllers import portal
from odoo import fields, http, _, tools


# from odoo.addons.mail.controllers.main import MailController
class CompanyVendorController(http.Controller):

    @http.route('/web_forms', type="http", auth="public", website=True)
    def le_webform(self):
        print('controller called............')
        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        partner = request.env.user.partner_id

        vals = {
            'countries': countries,
            'states': states,
            'partner': partner,
        }
        return http.request.render('rdp_vendor_registration_form.Vendor_Enquiry_Form', vals)

    @http.route('/samples', methods=['GET', 'POST', 'FILES'], type='http', auth='public', website=True)
    def vendor_enquiry_form(self, **kw):
        print('controller again called.........')
        additional_title = "Vendor Registration"
        vendor_type = "company"
        states = request.env['res.country.state'].sudo().search([])
        countries = request.env['res.country'].sudo().search([])
        product_categorys = request.env['product.category'].sudo().search([])
        error = {}
        if request.httprequest.method == 'POST':
            post_data = request.httprequest.form.to_dict()
            print('post data is validating')

            # Validate form data
            if not post_data.get('name'):
                error['name'] = "Please enter company name."
            if not post_data.get('vat'):
                error['vat'] = "Please enter GSTIN."
            if not post_data.get('email'):
                error['email'] = "Please enter email address."
            if not post_data.get('phone'):
                error['phone'] = "Please enter phone number."
            if not post_data.get('mobile'):
                error['mobile'] = "Please enter mobile number."
            if not post_data.get('street'):
                error['street'] = "Please enter street address."
            if not post_data.get('city'):
                error['city'] = "Please enter city."
            if not post_data.get('state_id'):
                error['state_id'] = "Please select state."
            if not post_data.get('country_id'):
                error['country_id'] = "Please select country."
            if not post_data.get('zipcode'):
                error['zipcode'] = "Please enter ZIP/Pincode."
            if not post_data.get('established_in'):
                error['established_in'] = "Please enter established in date."
            if not post_data.get('x_studio_company_turnover'):
                error['x_studio_company_turnover'] = "Please select revenue category."
            if not post_data.get('x_studio_last_2_yr_avg_revenue_in_crores'):
                error['x_studio_last_2_yr_avg_revenue_in_crores'] = "Please enter last 2 yr avg revenue."
            if not post_data.get('x_studio_social_contact_skypewechatother'):
                error['x_studio_social_contact_skypewechatother'] = "Please enter social contact."
            if not post_data.get('major_supplier'):
                error['major_supplier'] = "Please enter major suppliers."
            if not post_data.get('x_studio_top_5_customers_for_reference'):
                error['x_studio_top_5_customers_for_reference'] = "Please enter top 5 customers."
            if not post_data.get('x_studio_services'):
                error['x_studio_services'] = "Please enter services offered."
            if not post_data.get('comment'):
                error['comment'] = "Please enter additional comments."

            if not error:
                print('data is saving in dict')
                # Save form data
                model = request.env['res.partner']
                partner_values = {
                    'name': post_data['name'],
                    'email': post_data['email'],
                    'phone': post_data['phone'],
                    'mobile': post_data['mobile'],
                    'street': post_data['street'],
                    'street2': post_data['street2'],
                    'city': post_data['city'],
                    'state_id': int(post_data['state_id']),
                    'country_id': int(post_data['country_id']),
                    # 'zip': post_data['zipcode'],
                }

                # # Create a new contact
                #         new_contact = request.env['res.partner'].create(partner_values)
                #
                #     # # Link the contact to the CRM lead
                #     # new_contact.partner_id = new_contact.id
                #
                #         return http.request.make_response('Data Saved')
                #         print('error occured while saving data')
                #     return http.request.render('rdp_vendor_regitration_form.Vendor_Enquiry_Form')

                # Check if a contact with the same email already exists
                existing_contact = request.env['res.partner'].search([('email', '=', post_data['email'])], limit=1)

                # if existing_contact:
                #     # If the contact already exists, return the existing contact
                #     return http.request.make_response('Contact with the same email already exists.')

                # if existing_contact:
                #     # If the contact already exists, create a wizard and show the pop-up
                #     wizard = request.env['contact.exists.wizard'].create({
                #         'message': 'Contact with the same email already exists.',
                #     })
                #     return {
                #         'type': 'ir.actions.act_window',
                #         'res_model': 'contact.exists.wizard',
                #         'view_mode': 'form',
                #         'view_id': request.env.ref('rdp_vendor_registration_form.view_contact_exists_wizard_form').id,
                #
                #         # 'view_id': request.env.ref('rdp_vendor_registration_form.view_contact_exists_wizard_form').id,
                #         'target': 'new',
                #         'res_id': wizard.id,
                #     }
                if existing_contact:
                    # If the contact already exists, create a wizard and show the pop-up
                    wizard = request.env['contact.exists.wizard'].create({
                        'message': 'Contact with the same email already exists.',
                    })

                    # Render the view associated with the wizard
                    return http.request.render('rdp_vendor_registration_form.contact_exists_wizard_template', {
                        'wizard': wizard,
                    })

                # If no existing contact found, create a new one
                new_contact = request.env['res.partner'].create(partner_values)

                return http.request.make_response('Data Saved')
        return http.request.render('rdp_vendor_registration_form.Vendor_Enquiry_Form')
# ---------------

    # def _validate_and_fetch_gst_data(self, gst_number):
    #     # Implement your GST number validation and data fetching logic here
    #     # Make API request to the GST portal or perform any required validation
    #     # Return the GST data if valid, otherwise return None
    #
    #     # Example: Assume there is an API to validate GST number and fetch data
    #     api_url = '6b42cdabc535d5f2aa679038a83c25ff'                #GSTAPI KEY
    #     api_key = '462dec555ef9e99480037cc6883b3f080210b5bc'         # ODOOAPIKEY
    #     params = {'gst_number': gst_number, 'api_key': api_key}
    #
    #     response = requests.get(api_url, params=params)
    #
    #     if response.status_code == 200:
    #         gst_data = response.json()
    #         return gst_data
    #     else:
    #         return None

# ---------------
#
# def _validate_and_fetch_gst_data(self, gst_number):
#     """Validates a GST number and fetches corresponding data.
#
#     Args:
#         gst_number: The GST number to validate and fetch data for.
#
#     Returns:
#         A dictionary containing GST data if valid, otherwise None.
#     """
#
#     api_url = 'https://example.com/api/verify-gst'
#     api_key = '462dec555ef9e99480037cc6883b3f080210b5bc'
#     params = {'gst_number': gst_number, 'api_key': api_key}
#
#     try:
#         response = requests.get(api_url, params=params)
#         response.raise_for_status()  # Raise an exception for non-200 status codes
#
#         gst_data = response.json()
#         return gst_data
#     except requests.exceptions.RequestException as e:
#         # Handle potential request errors gracefully
#         print(f"Error fetching GST data: {e}")
#         return None
# def validate_gst_number_format(self, gst_number):
#     # Implement GST number format, length, and checksum validation rules
#     # Return True for valid, False for invalid
#     @api.onchange('gst_number')
#     def onchange_gst_number(self):
#         gst_data = self.validate_gst_number_api(self.gst_number)
#         if gst_data:
#             # Auto-fill other fields with GST data
#             self.name = gst_data.get('name')
#             self.address = gst_data.get('address')
#             # ...
#         else:
#             # Display an error message if invalid
#             self.error_message = 'Invalid GST number'

# # -----------------XML RPC---------------------------
#
# import xmlrpc.client
#
# url = 'http://localhost:8080'
# db = 'odoo17com'
# username = 'odoo17com'
# password = 'odoo17com'
#
# common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format('url'))
# uid = common.authenticate(db, username, password, {})
#
# models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format('url'))
#
# # Check Odoo server version
# server_version = common.version()
# print("Server Version:", server_version)
#
# # Check access rights for 'res.partner'
# # access_rights = models.execute_kw('odoo17com','odoo17com','odoo17com', 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})
# # print("Access Rights for 'res.partner':", access_rights)
#
# # Search for records in 'res.partner' where 'is_company' is True
# partner_ids = models.execute_kw(db, uid, password,  'res.partner', 'search', [[['is_company', '=', True]]])
# print("Company IDs:", partner_ids)
