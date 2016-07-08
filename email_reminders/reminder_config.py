# -*- encoding: utf-8 -*-
# Email reminder
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# reminder_config.py

import logging


class ReminderConfig:
    '''Class responsible in keep the reminder config.
    '''

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)

        self.action_name = config.get('reminder', 'action_name')
        self.reminder_template_name = config.get('reminder', 'reminder_template_name')
        self.summary_template_name = config.get('reminder', 'summary_template_name')
        self.tables = config.get('reminder', 'tables')
        self.fields = config.get('reminder', 'fields')
        self.filter = config.get('reminder', 'filter')
        self.attachment_url = config.get('reminder', 'attachment_url')
        self.send_resume_to = config.get('reminder', 'send_resume_to')
        self.update = config.get('reminder', 'update')

        return


    def print_config(self):
        self.logger.info('\nREMINDER config')
        self.logger.info('\taction_name: %s' % self.action_name)
        self.logger.info('\treminder_template_name: %s' % self.reminder_template_name)
        self.logger.info('\tsummary_template_name: %s' % self.summary_template_name)
        self.logger.info('\ttables: %s' % self.tables)
        self.logger.info('\tfields: %s' % self.fields)
        self.logger.info('\tfilter: %s' % self.filter)
        self.logger.info('\tattachment_url: %s' % self.attachment_url)
        self.logger.info('\tsend_resume_to: %s' % self.send_resume_to)
        self.logger.info('\tupdate: %s' % self.update)

        return
