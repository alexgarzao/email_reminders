# -*- encoding: utf-8 -*-
# Email reminder
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# send_mail.py

import mandrill


class SendMail:
    '''Class responsible in send the email using the mandrill.
    '''

    def __init__(self, mandrill_config):

    	self.mandrill_config = mandrill_config

        try:
            self.mandrill_client = mandrill.Mandrill(self.mandrill_config.api_key)
        except mandrill.Error, e:
            print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
            raise


    def send(self, email, name, content):
        '''Send the email.
        '''
        message = {
            'global_merge_vars': content,
            'google_analytics_campaign': self.mandrill_config.google_analytics_campaign,
            'google_analytics_domains': self.mandrill_config.google_analytics_domains,
            'headers': self.mandrill_config.headers,
            'important': False,
            'merge': True,
            'merge_language': 'handlebars',
            'metadata': self.mandrill_config.metadata,
            'to': [{'email': email, 'name': name, 'type': 'to'}],
            'track_clicks': True,
            'track_opens': True,
            'tracking_domain': True,
        }

        try:
            result = self.mandrill_client.messages.send_template(
                template_name=self.mandrill_config.template_name,
                template_content=None,
                message=message,
                async=False,
                ip_pool='Main Pool')

            return result[0]['status'] == 'sent', result[0]['reject_reason']
        except mandrill.Error, e:
            print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
            return False
