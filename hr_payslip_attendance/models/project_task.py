from odoo import models, fields, api, _


class Task(models.Model):
    _inherit = 'project.task'

    @api.model
    def _task_message_auto_subscribe_notify(self, users_per_task):
        # Utility method to send assignation notification upon writing/creation.
        template_id = self.env['ir.model.data']._xmlid_to_res_id('project.project_message_user_assigned',
                                                                 raise_if_not_found=False)
        template = self.env.ref('hr_payslip_attendance.project_task_email_template',
                                raise_if_not_found=False)
        if not template_id:
            return
        task_model_description = self.env['ir.model']._get(self._name).display_name
        for task, users in users_per_task.items():
            if not users:
                continue
            values = {
                'object': task,
                'model_description': task_model_description,
                'access_link': task._notify_get_action_link('view'),
            }
            for user in users:
                # Send email to assigned person
                email_values = {
                    'email_to': user.email_formatted,
                    'user_name': user.name,
                    'description': task.description if task.description else ''
                }

                values.update(assignee_name=user.sudo().name)
                assignation_msg = self.env['ir.qweb']._render('project.project_message_user_assigned', values,
                                                              minimal_qcontext=True)
                assignation_msg = self.env['mail.render.mixin']._replace_local_links(assignation_msg)

                task.message_notify(
                    subject=_('You have been assigned to %s', task.display_name),
                    body=assignation_msg,
                    partner_ids=user.partner_id.ids,
                    record_name=task.display_name,
                    email_layout_xmlid='mail.mail_notification_layout',
                    model_description=task_model_description,
                )
                template.with_context(email_values).send_mail(
                    task.id,
                    email_layout_xmlid='mail.mail_notification_layout'
                )

