# -*- coding: utf-8 -*-
{
    'name': "hr_payslip_attendance",
    'version': '1.0',
    'category': 'Payroll',
    'summary': 'Connect Attendance to Payslip',
    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'sale',
                'hr_attendance',
                'hr_payroll',
                'hr_contract',
                'hr_work_entry',
                'airo_overtime_request',
                'project_enterprise'
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/hr_payslip_attendance.xml',
        'views/hr_contract.xml',
        'data/hr_payslip_report.xml',
        'data/report_payslip_templates.xml',
        'data/ir_actions_report_templates_inherit.xml',
        'data/project_task_templates.xml',
        'data/financial_report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],
    'css': [],
    'installable': True,
    'application': True,
    'sequence': -100,
    'auto_install': False,
    'license': 'OPL-1'
}
