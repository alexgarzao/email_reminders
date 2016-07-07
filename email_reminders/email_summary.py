# -*- encoding: utf-8 -*-
# Email reminder
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# email_summary.py

from datetime import datetime


class EmailSummary:
    def __init__(self):
        self.start_time = datetime.now()
        self.sent_with_success = 0
        self.sent_with_error = 0
        self.finish_time = datetime.now()
        self.command_line_parameters = ''
        self.config_line_parameters = []
        self.query = ''
    def get(self):
        self.finish_time = datetime.now()
        email_summary = '''
Summary:
    Start: {}
    Records to process: {}
    Sent with success: {}
    Sent with error: {}
    Finish: {}
Details:
    Command line parameters: {}
    Config file parameters:
        {}
    Query filter used: {}
'''
        return email_summary.format(
            self.start_time,
            self.sent_with_success + self.sent_with_error,
            self.sent_with_success,
            self.sent_with_error,
            self.finish_time,
            self.command_line_parameters,
            'TO DO',
            self.query
        )
