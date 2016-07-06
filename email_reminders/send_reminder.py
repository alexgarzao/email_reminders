# -*- encoding: utf-8 -*-
# Email reminder
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# send_reminder.py

from send_mail import SendMail


class SendReminder:
    '''Class responsible in filter the data, to configure the template data and to send the email.
    '''

    def __init__(self, db_cursor, mandrill_config):
        self.db_cursor = db_cursor
        self.mandrill_config = mandrill_config

    def Send(self, reminder_config):
        '''Filter the data and send the reminder.
        '''
        query = 'SELECT %s FROM %s WHERE %s' % (reminder_config.fields, reminder_config.tables, reminder_config.filter)

        print 'QUERY=', query

        self.db_cursor.execute(query)

        send_mail = SendMail(self.mandrill_config)

        totalSent = 0
        totalError = 0

        fields = self.db_cursor.description

        for row in self.db_cursor:
            content = [{"name": x[0], "content": row[x[0]]} for x in fields]

            email = row['email']
            name = row['name']

            sent, reject_reason = send_mail.send(email, name, content)
            if sent == False:
                print('ERROR: Email {}. Reason: {}'.format(email, reject_reason))
                totalError += 1
                continue

            # Update record
            if reminder_config.update != '':
                self.db_cursor.execute(reminder_config.update, [row[reminder_config.update_field]])

            totalSent += 1

            print('OK: Email {}'.format(email))


        print('Sent with success: {} Fail: {}'.format(totalSent, totalError))

        return
