from odoo import tools
from odoo import models, fields, api, _


class HrPayslipAttendance(models.Model):
    _inherit = 'hr.contract'

    average_hours_per_day = fields.Float(related='resource_calendar_id.hours_per_day', store=True)
    is_undertime = fields.Boolean(string='Undertime Deduction', default=False)
