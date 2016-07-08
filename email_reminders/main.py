# -*- encoding: utf-8 -*-
# Email reminder
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# main.py

import argparse
import MySQLdb
import MySQLdb.cursors
import ConfigParser
import logging

from reminder_config import ReminderConfig
from mandrill_config import MandrillConfig
from send_reminder import SendReminder
from email_summary import EmailSummary
from send_mail import SendMail


class Main:
    '''Main class.
    '''

    def __init__(self):
        self.summary = EmailSummary()

    def run(self):
        '''Execute the program.
        '''

        self.__log_config()

        self.logger.info('Starting email reminder...')

        self.__parser_args()
        self.__load_config_file()
        self.__print_config()
        self.__db_connect()
        self.__send_reminder()
        self.__send_summary()

        self.logger.info('Reminder finishing...')

    def __log_config(self):
        logging.basicConfig(level=logging.INFO)

        self.logger = logging.getLogger(__name__)

    def __parser_args(self):
        '''Define the configuration list.
        '''
        parser = argparse.ArgumentParser(description='Send reminders throught Mandrill.')

        parser.add_argument(
                    '--reminder-config-file',
                    dest='config_filename',
                    action='store',
                    type=str,
                    help='Config file with reminder options',
                    required=True
        )

        self.args = parser.parse_args()

        self.logger.info('Command line configuration')
        self.logger.info('\tReminder config file: %s' % self.args.config_filename)

        self.summary.command_line_parameters = '--reminder-config-file=' + self.args.config_filename

    def __load_config_file(self):
        '''Load the config file specified in --reminder-config-file parameter.
        '''
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.args.config_filename)

    def __print_config(self):
        '''Print configuration.
        '''
        self.logger.info('\nDB config')
        self.logger.info('\thost: %s' % self.config.get('db', 'host'))
        self.logger.info('\tname: %s' % self.config.get('db', 'name'))
        self.logger.info('\tuser: %s' % self.config.get('db', 'user'))
        self.logger.info('\tpassword: %s' % self.config.get('db', 'password'))
        self.logger.info('\tport: %s' % self.config.getint('db', 'port'))

        self.logger.info('\nMANDRILL config')
        self.logger.info('\tapi_key: %s' % self.config.get('mandrill', 'api_key'))
        self.logger.info('\tgoogle_analytics_campaign: %s' % self.config.get('mandrill', 'google_analytics_campaign'))
        self.logger.info('\tgoogle_analytics_domains: %s' % self.config.get('mandrill', 'google_analytics_domains'))
        self.logger.info('\treply_to: %s' % self.config.get('mandrill', 'reply_to'))
        self.logger.info('\twebsite: %s' % self.config.get('mandrill', 'website'))

        self.logger.info('\nREMINDER config')
        self.logger.info('\taction_name: %s' % self.config.get('reminder', 'action_name'))
        self.logger.info('\treminder_template_name: %s' % self.config.get('reminder', 'reminder_template_name'))
        self.logger.info('\tsummary_template_name: %s' % self.config.get('reminder', 'summary_template_name'))
        self.logger.info('\ttables: %s' % self.config.get('reminder', 'tables'))
        self.logger.info('\tfields: %s' % self.config.get('reminder', 'fields'))
        self.logger.info('\tfilter: %s' % self.config.get('reminder', 'filter'))
        self.logger.info('\tsend_resume_to: %s' % self.config.get('reminder', 'send_resume_to'))
        self.logger.info('\tupdate: %s' % self.config.get('reminder', 'update'))
        self.logger.info('\tupdate_field: %s' % self.config.get('reminder', 'update_field'))

        self.logger.info('\n')

    def __db_connect(self):
        '''Connect with the database.
        '''
        self.db_cnx = MySQLdb.connect(
            user=self.config.get('db', 'user'),
            db=self.config.get('db', 'name'),
            host=self.config.get('db', 'host'),
            passwd=self.config.get('db', 'password'),
            port=self.config.getint('db', 'port'),
            unix_socket='tcp'
        )

    def __send_reminder(self):
        '''Send the reminder.
        '''
        mandrill_config = MandrillConfig(
            api_key = self.config.get('mandrill', 'api_key'),
            google_analytics_campaign = self.config.get('mandrill', 'google_analytics_campaign'),
            google_analytics_domains =  [self.config.get('mandrill', 'google_analytics_domains')],
            headers = {'Reply-To': self.config.get('mandrill', 'reply_to')},
            metadata = {'website': self.config.get('mandrill', 'website')},
        )

        reminder_config = ReminderConfig(
            action_name = self.config.get('reminder', 'action_name'),
            reminder_template_name = self.config.get('reminder', 'reminder_template_name'),
            summary_template_name = self.config.get('reminder', 'summary_template_name'),
            tables = self.config.get('reminder', 'tables'),
            fields = self.config.get('reminder', 'fields'),
            filter = self.config.get('reminder', 'filter'),
            send_resume_to = self.config.get('reminder', 'send_resume_to'),
            update = self.config.get('reminder', 'update'),
            update_field = self.config.get('reminder', 'update_field')
        )

        db_cursor = self.db_cnx.cursor(MySQLdb.cursors.DictCursor)

        send_reminder = SendReminder(db_cursor, mandrill_config)
        success, error, query = send_reminder.Send(reminder_config)

        if reminder_config.update != '':
            self.db_cnx.commit()

        self.summary.sent_with_success = success
        self.summary.sent_with_error = error
        self.summary.query = query

        return

    def __send_summary(self):
        '''Send the reminder.
        '''
        mandrill_config = MandrillConfig(
            api_key = self.config.get('mandrill', 'api_key'),
            google_analytics_campaign = self.config.get('mandrill', 'google_analytics_campaign'),
            google_analytics_domains =  [self.config.get('mandrill', 'google_analytics_domains')],
            headers = {'Reply-To': self.config.get('mandrill', 'reply_to')},
            metadata = {'website': self.config.get('mandrill', 'website')},
        )

        self.summary.mandrill_config = mandrill_config

        self.logger.info('Summary:\n%s\n' % self.summary.get())

        sent, reject_reason = self.summary.send(self.config.get('reminder', 'send_resume_to'), self.config.get('reminder', 'summary_template_name'))

        if sent == True:
            self.logger.info('Summary sent with success')
        else:
            self.logger.error('Summary rejected: reason=%s' % reject_reason)

        return


if __name__ == "__main__":
    main = Main()
    main.run()
