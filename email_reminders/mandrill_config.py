# -*- encoding: utf-8 -*-
# Email reminder
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# mandrill_config.py

class MandrillConfig:
    '''Class responsible in keep the mandrill config.
    '''

    def __init__(
            self, api_key, template_name,
            track_clicks = True, track_opens = True, tracking_domain = True,
            google_analytics_campaign = None, google_analytics_domains = None, headers = None, metadata = None):
        self.api_key = api_key
        self.track_clicks = track_clicks
        self.track_opens = track_opens
        self.tracking_domain = tracking_domain
        self.template_name = template_name
        self.google_analytics_campaign = google_analytics_campaign
        self.google_analytics_domains = google_analytics_domains
        self.headers = headers
        self.metadata = metadata
