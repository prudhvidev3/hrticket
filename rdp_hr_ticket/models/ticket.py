from odoo import api, fields, models, _
from datetime import date, datetime
import time
class HRTicket(models.Model):
    _name = "hr.ticket"
    _description = "HR Ticket"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = 'id desc'

    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, states={'draft': [('readonly', False)]}, readonly=True)
    employee_name_id = fields.Many2one('hr.employee', "Employee Name", store=True, readonly='1',  compute="compute_employee_name")
    reporting_manager_id = fields.Many2one('hr.employee', string="Reporting Manager", track_visibility='always')
    department_id = fields.Many2one('hr.department', string="Department", track_visibility='always')
    parent_department_id = fields.Many2one('hr.department', string="Parent Department", track_visibility='always')
    request = fields.Html(string="Brief About Ticket", required=True, track_visibility="always")
    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'), track_visibility='always')
    open_days_new_stage = fields.Integer(string='Open Days New Stage', compute="calculate_open_days_new_stage", track_visibility='always')
    closed_date = fields.Datetime(string='closed date', track_visibility='always')
    spoc_id = fields.Many2one("hr.employee", 'SPOC', track_visibility='always')
    state = fields.Selection([('new', 'New'),('in_progress', 'In Progress'),('resolve', 'Resolved'),('close', 'Closed')], string='Status', default='new', track_visibility='always')
    ticket_category = fields.Selection([('leave_query', 'Leave Query'),
                                        ('pay_slip_enquiry', 'Pay Slip Enquiry'),
                                        ('salary_query', 'Salary Query'),
                                        ('incentive_query', 'Incentive Query'),
                                        ('employee_onboarding_requirements_quiry', 'Employee Onboarding Requirements Quiry'),
                                        ('performance_review', 'Performance Review'),
                                        ('hr_policy_inquiry', 'HR Policy Inquiry'),
                                        ('workplace_harassment_conflict', 'Workplace Harassment/Conflict'),
                                        ('training_and_development_needs', 'Training And Development Needs'),
                                        ('employee_grievance', 'Employee Grievance'),
                                        ('employee_recognition', 'Employee Recognition'),
                                        ('performance_improvement_plan', 'Performance Improvement Plan (PIP)'),
                                        ('workplace_safety', 'Workplace Safety'),
                                        ('off_boarding_exit_related', 'Offboarding/Exit related'),
                                        ('hr_system_access', 'HR System Access'),
                                        ('time_and_attendance_support', 'Time And Attendance Support'),
                                        ('hr_feedback_suggestion', 'HR Feedback/Suggestion'),
                                        ('job_posting_referral_status', 'Job Posting/Referral Status'),
                                        ('hr_admin_related', 'HR Admin Related'),('new hiring requirement', 'New Hiring Requirement'),('replacement requirement.', 'Replacemment Requirement'),
                                        ('others', 'Others')], string="Ticket Category", track_visibility='always')
    hr_spoc_assigned_to_id = fields.Many2one('res.users', 'HR Spoc Assigned To', track_visibility='always')
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'High'), ('3', 'Very High')], string='Priority', track_visibility='always')

    @api.model
    def create(self, vals):
        vals.update({
            'name': self.env['ir.sequence'].next_by_code('hr.ticket.sequence')
        })
        res = super(HRTicket, self).create(vals)
        template_id = self.env['ir.model.data'].get_object_reference('rdp_hr_ticket', 'hr_ticket_app_employee_notification')[1]
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(res.id, force_send=True)
        return res

    @api.multi
    def action_to_in_progress(self):
        self.state = 'in_progress'

    @api.multi
    def action_to_resolved(self):
        template_id = self.env.ref("rdp_hr_ticket.automated_response_to_the_employee_who_raised_ticket")
        template_id.send_mail(self.id, force_send=True)
        self.state = 'resolve'

    @api.multi
    def action_to_close(self):
        self.closed_date = datetime.now()
        template_id = self.env.ref("rdp_hr_ticket.automated_response_to_the_ticket_closed_notification_to_employee")
        template_id.send_mail(self.id, force_send=True)
        self.state = 'close'

    @api.multi
    def action_set_new(self):
        self.write({'state': 'new'})

    @api.multi
    def calculate_open_days_new_stage(self):
        for rec in self:
            if rec.state == 'new':
                rec.open_days_new_stage = (datetime.today() - rec.create_date).days

    @api.depends('user_id')
    def compute_employee_name(self):
        for rec in self:
            employee = rec.env['hr.employee'].sudo().search([('user_id', '=', rec.env.uid)])
            rec.employee_name_id = employee.id

    @api.onchange('employee_name_id')
    def onchange_employee_name_id(self):
        for rec in self:
            if rec.employee_name_id:
                rec.reporting_manager_id = rec.employee_name_id.parent_id
                rec.spoc_id = rec.employee_name_id.coach_id
                rec.department_id = rec.employee_name_id.department_id
                rec.parent_department_id = rec.employee_name_id.parent_department_id









