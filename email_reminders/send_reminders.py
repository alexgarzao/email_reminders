# -*- encoding: utf-8 -*-
# Email reminder
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# send_reminder.py

import requests

from send_mail import SendMail
import logging
from string import Template
import base64


class SendReminders:
    '''Class responsible in filter the data, to configure the template data and to send the email.
    '''

    def __init__(self, db_cursor, mandrill_config):
        self.db_cursor = db_cursor
        self.mandrill_config = mandrill_config

        self.logger = logging.getLogger(__name__)

    def Send(self, reminder_config):
        '''Filter the data and send the reminder.
        '''
        query = reminder_config.get_query()

        self.logger.info('QUERY=%s' % query)

        total_records = self.db_cursor.execute(query)

        self.logger.info('Records in cursor set: %d' % total_records)

        send_mail = SendMail(self.mandrill_config)

        total_sent = 0
        total_error = 0

        fields = self.db_cursor.description

        for row in self.db_cursor:
            content = [{"name": x[0], "content": row[x[0]]} for x in fields]

            email = row['email']
            name = row['name']

            attachments = None

            if reminder_config.attachment_url != '':
                attachment_url_strings = {x[0]: row[x[0]] for x in fields}
                attachment_url = Template(reminder_config.attachment_url).safe_substitute(attachment_url_strings)
                self.logger.info('URL=%s' % attachment_url)
            	attachment_content = requests.get(attachment_url)
                self.logger.info('content size=%d' % len(attachment_content.content))
            	encoded_content = base64.b64encode(attachment_content.content)

            	attachments = [
            	    {
            	        'content': encoded_content,
            	        'name': 'boleto_atar_band.pdf',
            	        'type': 'application/pdf'
            	    }
            	]

            sent, reject_reason = send_mail.send_using_template(email, name, reminder_config.reminder_template_name, content, attachments)
            if sent == False:
                self.logger.error('Email {}. Reason: {}'.format(email, reject_reason))
                total_error += 1
                continue

            # Update record
            if reminder_config.update != '':
                update_strings = {x[0]: row[x[0]] for x in fields}
                update_sql = Template(reminder_config.update).safe_substitute(update_strings)
                self.logger.info('UPDATE SQL=%s' % update_sql)

                self.db_cursor.execute(update_sql)

            total_sent += 1

            self.logger.info('OK: Email {}'.format(email))

        self.logger.info('Sent with success: {} Fail: {}'.format(total_sent, total_error))

        return total_sent, total_error, query
