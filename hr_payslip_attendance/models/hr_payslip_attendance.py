from odoo import tools
from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval

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

    def _generate_pdf(self):
        mapped_reports = self._get_pdf_reports()
        attachments_vals_list = []
        generic_name = _("Payslip")
        template = self.env.ref('hr_payslip_attendance.mail_template_new_payslip_inherit', raise_if_not_found=False)
        for report, payslips in mapped_reports.items():
            for payslip in payslips:
                pdf_content, dummy = self.env['ir.actions.report'].sudo()._render_qweb_pdf(report, payslip.id)
                if report.print_report_name:
                    pdf_name = safe_eval(report.print_report_name, {'object': payslip})
                else:
                    pdf_name = generic_name
                attachments_vals_list.append({
                    'name': pdf_name,
                    'type': 'binary',
                    'raw': pdf_content,
                    'res_model': payslip._name,
                    'res_id': payslip.id
                })

                # Send email to employees
                if template:
                    data_id = self.env['ir.attachment'].sudo().create({
                    'name': pdf_name,
                    'type': 'binary',
                    'raw': pdf_content,
                    'res_model': payslip._name,
                    'res_id': payslip.id
                    })
                    template.attachment_ids = [(6, 0, [data_id.id])]
                    template.send_mail(payslip.id, email_layout_xmlid='mail.mail_notification_light')
        self.env['ir.attachment'].sudo().create(attachments_vals_list)
