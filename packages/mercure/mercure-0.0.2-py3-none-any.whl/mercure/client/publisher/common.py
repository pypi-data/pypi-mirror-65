from requests import Session
from requests.exceptions import RequestException

from mercure.client.publisher.base import (
    DEFAULT_EVENT_TYPE_MAX_SIZE,
    DEFAULT_EVENT_MESSAGE_MAX_SIZE,
    BasePublisherClient,
)


class MercurePublisherClient(BasePublisherClient):
    def __init__(self,
                 hub_url,
                 event_type_max_size=DEFAULT_EVENT_TYPE_MAX_SIZE,
                 event_message_size=DEFAULT_EVENT_MESSAGE_MAX_SIZE,
                 channel_generation_salt='',
                 transport_session=None):
        super().__init__(hub_url, event_type_max_size, event_message_size,
                         channel_generation_salt)
        self.session = transport_session or Session()

    def _invoke_request(self, channel_name, payload):
        try:
            self.session.post(
                url=self.hub_url,
                params={'id': channel_name},
                data=payload,
            )
        except RequestException:
            # We don't guarantee delivery, failing silently
            pass
