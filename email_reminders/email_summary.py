# -*- encoding: utf-8 -*-
# Email reminder
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# email_summary.py

from datetime import datetime
from send_mail import SendMail


class EmailSummary:
    def __init__(self):
    	self.mandrill_config = None

        self.start_time = datetime.now()
        self.sent_with_success = 0
        self.sent_with_error = 0
        self.finish_time = datetime.now()
        self.command_line_parameters = ''
        self.config_line_parameters = []
        self.query = ''

        return

    def send(self, send_resume_to, template_name):
        send_mail = SendMail(self.mandrill_config)

        self.finish_time = datetime.now()

        content = [
            {'name': 'start-time', 'content': self.start_time.strftime("%Y-%m-%d %H:%M:%S")},
            {'name': 'records-processed', 'content': self.sent_with_success + self.sent_with_error},
            {'name': 'success', 'content': self.sent_with_success},
            {'name': 'error', 'content': self.sent_with_error},
            {'name': 'finish-time', 'content': self.finish_time.strftime("%Y-%m-%d %H:%M:%S")},
            {'name': 'command-line-parameters', 'content': self.command_line_parameters},
            {'name': 'query-filter-used', 'content': self.query}
        ]

        sent, reject_reason = send_mail.send_using_template(
            send_resume_to, 
            'Reminder',
            template_name,
            content
        )

        return sent, reject_reason


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
