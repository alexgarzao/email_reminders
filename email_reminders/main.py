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
from send_reminders import SendReminders
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
        self.__send_reminders()
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

        self.mandrill_config = MandrillConfig(self.config)
        self.reminder_config = ReminderConfig(self.config)

    def __print_config(self):
        '''Print configuration.
        '''
        self.logger.info('\nDB config')
        self.logger.info('\thost: %s' % self.config.get('db', 'host'))
        self.logger.info('\tname: %s' % self.config.get('db', 'name'))
        self.logger.info('\tuser: %s' % self.config.get('db', 'user'))
        self.logger.info('\tpassword: %s' % self.config.get('db', 'password'))
        self.logger.info('\tport: %s' % self.config.getint('db', 'port'))

        self.mandrill_config.print_config()
        self.reminder_config.print_config()

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

    def __send_reminders(self):
        '''Send the reminders.
        '''

        db_cursor = self.db_cnx.cursor(MySQLdb.cursors.DictCursor)

        send_reminders = SendReminders(db_cursor, self.mandrill_config)
        success, error, query = send_reminders.Send(self.reminder_config)

        if self.reminder_config.update != '':
            self.db_cnx.commit()

        self.summary.sent_with_success = success
        self.summary.sent_with_error = error
        self.summary.query = query

        return

    def __send_summary(self):
        '''Send the reminder.
        '''
        self.summary.mandrill_config = self.mandrill_config

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
