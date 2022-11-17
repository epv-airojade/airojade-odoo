from odoo import tools
from odoo import models, fields, api, _


class HrPayslipAttendance(models.Model):
    _inherit = 'hr.payslip'

    attendance_ids = fields.One2many('hr.attendance', 'employee_id', compute='_onchange_period_attendance',
                                     readonly=True, string='Attendance')

    overtime_ids = fields.One2many('airo.overtime.request', 'employee_id', compute='_onchange_period_attendance',
                                     readonly=True, string='Attendance')

    @api.depends('date_from', 'date_to')
    def _onchange_period_attendance(self):
        for rec in self:
            rec.attendance_ids = self.env['hr.attendance'].search([('check_in', '>=', rec.date_from), ('check_out', '<=', rec.date_to), ('employee_id' , '=', rec.employee_id.id)])
            rec.overtime_ids = self.env['airo.overtime.request'].search([('date_from', '>=', rec.date_from), ('date_to', '<=', rec.date_to), ('employee_id' , '=', rec.employee_id.id), ('state', '=', 'approved')])
