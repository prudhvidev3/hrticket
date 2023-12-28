from odoo import models, fields, api

class YourCustomLead(models.Model):
    _inherit = 'res.partner'

    vat = fields.Char(string='GSTIN')
    website = fields.Char(string='website')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street2')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')
    # zipcode = fields.Char(string='ZIP/Pincode')
    # established_in = fields.Date(string='Established In')

    # x_studio_last_2_yr_avg_revenue_in_crores = fields.Float(string='Last 2 Yr Avg Revenue')


