# -*- coding: utf-8 -*-
import io
import json
from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.tools import date_utils

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class TravelManagementReport(models.TransientModel):
    """Class defined for creating wizard for report"""
    _name = 'sample.submission.report'
    _description = 'sample submission Report wizard'

    date_from = fields.Date(string="Date from",
                            help="Filter the report with the specified to date")
    date_to = fields.Date(string="Date to",
                          help="Filter the report with the specified from date")

    def create_pdf(self):
        """Function defined for creating PDF report on the button"""
        if self.date_from > self.date_to:
            raise ValidationError('Start Date must be less than End Date')

        query = """select p.name as customer,t.name,t.date_of_submission,t.reference,
                    t.price,t.discount,t.vat from sample_submission as t
                    INNER JOIN res_partner as p on  p.id=t.partner_id
                    where 1=1"""
        if self.date_to:
            query += """and t.date_of_submission <= '%s'""" % self.date_to
        if self.date_from:
            query += """and t.date_of_submission >= '%s'""" % self.date_from
        self.env.cr.execute(query)
        submission_data = self.env.cr.dictfetchall()
        data = {'form_data': self.read()[0],
                'submission_data': submission_data}
        return self.env.ref('sample_submission.action_report_sample_submission').report_action(self, data=data)

    def print_xlsx(self):
        """Function defined for creating XLSX report on button click"""
        if self.date_from > self.date_to:
            raise ValidationError('Start Date must be less than End Date')
        query = """select p.name as customer,t.name,t.date_of_submission,t.reference,
                            t.price,t.discount,t.vat from sample_submission as t
                            INNER JOIN res_partner as p on  p.id=t.partner_id
                            where 1=1"""
        if self.date_to:
            query += """and t.date_of_submission <= '%s'""" % self.date_to
        if self.date_from:
            query += """and t.date_of_submission >= '%s'""" % self.date_from
        self.env.cr.execute(query)
        submission_data = self.env.cr.dictfetchall()
        data = {'form_data': self.read()[0],
                'submission_data': submission_data}
        self.env.cr.execute(query)
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'sample.submission.report',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """Function defined for XLSX report view"""
        from_date = data['form_data']['date_from']
        to_date = data['form_data']['date_to']
        submission_data = data['submission_data']
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format(
            {'font_size': '12px', 'bold': True, 'align': 'center'})
        sheet.merge_range('I2:P3', "Sample Submission Report", head)
        sheet.merge_range('A7:B7', 'From Date:', txt)
        if self.date_from:
            sheet.merge_range('C7:D7', from_date, cell_format)
        sheet.merge_range('A8:B8', 'To Date:', txt)
        if self.date_to:
            sheet.merge_range('C8:D8', to_date, cell_format)
        sheet.write('B12', 'Sl. No', txt)
        sheet.merge_range('C12:E12', 'Reference', txt)
        sheet.merge_range('F12:H12', 'Name', txt)
        sheet.merge_range('I12:J12', 'Customer', txt)
        sheet.merge_range('K12:L12', 'Date', txt)
        sheet.merge_range('M12:N12', 'Price', txt)
        sheet.merge_range('O12:P12', 'Discount', txt)
        sheet.merge_range('Q12:R12', 'VAT', txt)
        sl_no = 0
        row = 12
        for rec in submission_data:
            sl_no += 1
            sheet.write(row, 1, sl_no, cell_format)
            sheet.merge_range(row, 2, row, 4, rec['reference'],
                              cell_format)
            sheet.merge_range(row, 5, row, 7,
                              rec['name'], cell_format)
            sheet.merge_range(row, 8, row, 9, rec['customer'], cell_format)
            sheet.merge_range(row, 10, row, 11, rec['date_of_submission'], cell_format)
            sheet.merge_range(row, 12, row, 13, rec['price'], cell_format)
            sheet.merge_range(row, 14, row, 15, rec['discount'], cell_format)
            sheet.merge_range(row, 16, row, 17, rec['vat'], cell_format)
            row += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
