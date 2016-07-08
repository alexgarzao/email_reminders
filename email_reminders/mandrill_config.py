# -*- encoding: utf-8 -*-
# Email reminder
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# mandrill_config.py

import logging


class MandrillConfig:
    '''Class responsible in keep the mandrill config.
    '''

    def __init__(self, config, track_clicks = True, track_opens = True, tracking_domain = True):

        self.logger = logging.getLogger(__name__)

        self.api_key = config.get('mandrill', 'api_key')
        self.google_analytics_campaign = config.get('mandrill', 'google_analytics_campaign')
        self.google_analytics_domains =  [config.get('mandrill', 'google_analytics_domains')]
        self.headers = {'Reply-To': config.get('mandrill', 'reply_to')}
        self.metadata = {'website': config.get('mandrill', 'website')}

        self.track_clicks = track_clicks
        self.track_opens = track_opens
        self.tracking_domain = tracking_domain

        return


    def print_config(self):
        self.logger.info('\nMANDRILL config')
        self.logger.info('\tapi_key: %s' % self.api_key)
        self.logger.info('\tgoogle_analytics_campaign: %s' % self.google_analytics_campaign)
        self.logger.info('\tgoogle_analytics_domains: %s' % self.google_analytics_domains)
        self.logger.info('\reply_to: %s' % self.headers)
        self.logger.info('\twebsite: %s' % self.metadata)

        return
