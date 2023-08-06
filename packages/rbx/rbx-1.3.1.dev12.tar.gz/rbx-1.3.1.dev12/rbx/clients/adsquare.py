import logging

import arrow

from . import Client, ClientException, HttpAuth

logger = logging.getLogger('rbx.clients.adsquare')


class AdsquareClient(Client):
    """Client for adsquare API.

    The API documentation can be found on the Platform wiki:
    https://github.com/rockabox/rbx/wiki/adsquare

    """
    AUTH_PATH = 'auth/login'
    ENDPOINT = 'https://amp.adsquare.com/api/v1/'
    STANDARD_COMPANY_ID = '588b6428e4b0d7d5f6895bd1'
    TIME_FORMAT = 'YYYY-MM-DDTHH:mm:ss.SSS[Z]'

    def __init__(self, company_id, dsp_id):
        super().__init__()
        self.company_id = company_id
        self.dsp_id = dsp_id

    @property
    def auth(self):
        """adsquare uses Digest Authentication."""
        return HttpAuth(self.token, key='X-AUTH-TOKEN')

    def create_config(self, country_code, name, start_date, end_date):
        """Create a new observation configuration.

        The start and end date are expected to be in ISO 8601, though any format understood by
        Arrow will work.
        """
        path = f'measurement/configs/byCompany/{self.company_id}'
        response = self.request('post', path, data={
            'dspId': self.dsp_id,
            'countryCode': country_code,
            'name': name,
            'active': True,
            'observationMode': 'full',
            'radiusInMeter': 50,
            'validFrom': arrow.get(start_date).format(self.TIME_FORMAT),
            'validTo': arrow.get(end_date).format(self.TIME_FORMAT),
        })
        return response['id']

    def disable_webhook(self, config_id):
        """Disable the registered webhook for the given configuration ID."""
        self.register_webhook(config_id, disable=True)

    def list_segments(self):
        """List all segments available.

        According to the documentation, there is no pagination on this endpoint, so we expect the
        full list to be returned with a single call.

        See: https://docs.adsquare.com/#!/enrichmentMetaApi/getEnrichmentAudiences_1
        """
        path = f'enrichmentMeta/audiences/{self.dsp_id}'
        response = self.request('get', path, data={'namev2': 'true'})

        return [{
            'company_id': audience['companyId'],
            'country': audience['countryCode'],
            'cpm': audience['cpm'],
            'currency': audience['currency'],
            'id': audience['audienceId'],
            'name': audience['name'],
            'owner': 'Standard' if audience['companyId'] == self.STANDARD_COMPANY_ID else 'Custom',
            'type': audience['type'],
        } for audience in response['audiences']]

    def pause_config(self, config_id):
        """Pause the given configuration."""
        self.update_config(config_id=config_id, active=False)

    def register_webhook(self, config_id, disable=False, feedback_url=None):
        """Register a Feedback URL webhook with adsquare for the given configuration ID.

        The same method can be used to re-enable an existing/disabled webhook.
        """
        data = {
            'enabled': not disable,
            'method': 'post',
            'contentType': 'csv',
        }
        if feedback_url:
            data['feedbackURL'] = feedback_url

        if not disable and not feedback_url:
            raise ClientException('Cannot register a webhook without a URL')

        return self.request('post', f'measurement/configs/{config_id}/feedback', data=data)

    def resume_config(self, config_id):
        """Resume the given configuration."""
        self.update_config(config_id=config_id, active=True)

    def update_config(self, config_id, active=None, start_date=None, end_date=None):
        """Update the given configuration ID.

        Only active and start/end dates can be changed.
        """
        data = {}

        if active is not None:
            data['active'] = active

        if start_date:
            data['validFrom'] = arrow.get(start_date).format(self.TIME_FORMAT)

        if end_date:
            data['validTo'] = arrow.get(end_date).format(self.TIME_FORMAT)

        return self.request('post', f'measurement/configs/{config_id}', data=data)

    def upload_config(self, config_id, points):
        """Upload a list of site locations to the given configuration.

        The points is expected to be a list of (lat, long) tuples as floating values.
        """
        data = ['id,lon,lat']
        for i, point in enumerate(points):
            data.append(f'{i},{point[1]},{point[0]}')

        # Make sure the payload has a trailing newline
        data.append('')

        self.request('put', f'measurement/configs/{config_id}/dataset/poi', data='\n'.join(data))
