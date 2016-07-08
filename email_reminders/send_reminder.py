# -*- encoding: utf-8 -*-
# Email reminder
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# send_reminder.py

from send_mail import SendMail
import logging


class SendReminder:
    '''Class responsible in filter the data, to configure the template data and to send the email.
    '''

    def __init__(self, db_cursor, mandrill_config):
        self.db_cursor = db_cursor
        self.mandrill_config = mandrill_config

        self.logger = logging.getLogger(__name__)

    def Send(self, reminder_config):
        '''Filter the data and send the reminder.
        '''
        query = 'SELECT %s FROM %s WHERE %s' % (reminder_config.fields, reminder_config.tables, reminder_config.filter)

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

            sent, reject_reason = send_mail.send_using_template(email, name, reminder_config.reminder_template_name, content)
            if sent == False:
                self.logger.error('Email {}. Reason: {}'.format(email, reject_reason))
                total_error += 1
                continue

            # Update record
            if reminder_config.update != '':
                self.db_cursor.execute(reminder_config.update, [row[reminder_config.update_field]])

            total_sent += 1

            self.logger.info('OK: Email {}'.format(email))

        self.logger.info('Sent with success: {} Fail: {}'.format(total_sent, total_error))

        return total_sent, total_error, query
