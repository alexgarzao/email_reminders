# -*- encoding: utf-8 -*-
# Email reminder
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# main.py

import argparse
import MySQLdb
import MySQLdb.cursors
import ConfigParser

from reminder_config import ReminderConfig
from mandrill_config import MandrillConfig
from send_reminder import SendReminder


class Main:
    '''Main class.
    '''

    def run(self):
        '''Execute the program.
        '''
        print 'Starting email reminder...'

        self.__parser_args()
        self.__load_config_file()
        self.__print_config()
        self.__db_connect()
        self.__send_reminder()

        print 'Reminder finishing...'

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

        print 'Command line configuration'
        print '\tReminder config file: %s' % self.args.config_filename

    def __load_config_file(self):
        '''Load the config file specified in --reminder-config-file parameter.
        '''
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.args.config_filename)

    def __print_config(self):
        '''Print configuration.
        '''
        print '\nDB config'
        print '\thost: %s' % self.config.get('db', 'host')
        print '\tname: %s' % self.config.get('db', 'name')
        print '\tuser: %s' % self.config.get('db', 'user')
        print '\tpassword: %s' % self.config.get('db', 'password')
        print '\tport: %s' % self.config.getint('db', 'port')

        print '\nMANDRILL config'
        print '\tapi_key: %s' % self.config.get('mandrill', 'api_key')
        print '\ttemplate_name: %s' % self.config.get('mandrill', 'template_name')
        print '\tgoogle_analytics_campaign: %s' % self.config.get('mandrill', 'google_analytics_campaign')
        print '\tgoogle_analytics_domains: %s' % self.config.get('mandrill', 'google_analytics_domains')
        print '\treply_to: %s' % self.config.get('mandrill', 'reply_to')
        print '\twebsite: %s' % self.config.get('mandrill', 'website')

        print '\nREMINDER config'
        print '\taction_name: %s' % self.config.get('reminder', 'action_name')
        print '\ttables: %s' % self.config.get('reminder', 'tables')
        print '\tfields: %s' % self.config.get('reminder', 'fields')
        print '\tfilter: %s' % self.config.get('reminder', 'filter')
        print '\tsend_resume_to: %s' % self.config.get('reminder', 'send_resume_to')
        print '\tupdate: %s' % self.config.get('reminder', 'update')
        print '\tupdate_field: %s' % self.config.get('reminder', 'update_field')

        print '\n'

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
            template_name = self.config.get('mandrill', 'template_name'),
            google_analytics_campaign = self.config.get('mandrill', 'google_analytics_campaign'),
            google_analytics_domains =  [self.config.get('mandrill', 'google_analytics_domains')],
            headers = {'Reply-To': self.config.get('mandrill', 'reply_to')},
            metadata = {'website': self.config.get('mandrill', 'website')},
        )

        reminder_config = ReminderConfig(
            action_name = self.config.get('reminder', 'action_name'),
            tables = self.config.get('reminder', 'tables'),
            fields = self.config.get('reminder', 'fields'),
            filter = self.config.get('reminder', 'filter'),
            send_resume_to = self.config.get('reminder', 'send_resume_to'),
            update = self.config.get('reminder', 'update'),
            update_field = self.config.get('reminder', 'update_field')
        )

        db_cursor = self.db_cnx.cursor(MySQLdb.cursors.DictCursor)

        send_reminder = SendReminder(db_cursor, mandrill_config)
        send_reminder.Send(reminder_config)

        if reminder_config.update != '':
            self.db_cnx.commit()

        return


if __name__ == "__main__":
    main = Main()
    main.run()
