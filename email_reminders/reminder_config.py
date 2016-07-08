# -*- encoding: utf-8 -*-
# Email reminder
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# reminder_config.py


class ReminderConfig:
    '''Class responsible in keep the reminder config.
    '''

    def __init__(self, action_name, reminder_template_name, summary_template_name, tables, fields, filter, send_resume_to, update, update_field):
        self.action_name = action_name
        self.reminder_template_name = reminder_template_name
        self.summary_template_name = summary_template_name
        self.tables = tables
        self.fields = fields
        self.filter = filter
        self.send_resume_to = send_resume_to
        self.update = update
        self.update_field = update_field
