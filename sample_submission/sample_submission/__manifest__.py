# -*- coding: utf-8 -*-
{
    "name": "Sample Submission",
    "summary": """ Sample Submission """,
    "category": "Sales",
    "version": "16.0.1.0.0",
    "author": "ABDUL HAKEEM",
    "license": "LGPL-3",
    "description": """  This app aims to streamline the management of sample submissions,
             connect customers to submission forms, keep track of materials as products related 
             to sample-submission,and generate invoices. Additionally, the app will support the 
             generation of PDF and Excel reports with specific data """,
    "depends": ['base', 'product','contacts', 'account'],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/sample_submission_view.xml',
        'wizards/material_required_wizard_view.xml',
        "views/popup_views.xml",
        'reports/sample_report_view.xml',
        'reports/report_template.xml',
        'reports/report.xml',
        'views/menu.xml',
    ],
    'assets': {
            'web.assets_backend': [
                'sample_submission/static/src/js/action_manager.js']
        },
    "application": True,
    "installable": True,
    "auto_install": False,
}
