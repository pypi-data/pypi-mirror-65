from json import dumps

from requests import Session

from mercure.client.publisher.base import (
    DEFAULT_EVENT_TYPE_SIZE,
    DEFAULT_EVENT_MESSAGE_SIZE,
    BasePublisherClient,
)


class MercurePublisherClient(BasePublisherClient):
    def __init__(self, 
                 hub_url,
                 event_type_size=DEFAULT_EVENT_TYPE_SIZE,
                 event_message_size=DEFAULT_EVENT_MESSAGE_SIZE,
                 channel_generation_salt='',
                 transport_session=None):
        super().__init__(hub_url, event_type_size, event_message_size,
                         channel_generation_salt)
        self.session = transport_session or Session()

    def _invoke_request(self, channel_name, event_type, event_message):
        message = {'event_type': event_type, 'event_message': event_message}
        try:
            self.session.post(
                url=self.hub_url,
                params={'id': channel_name},
                data=dumps(dumps(message)),
            )
        except Exception:
            pass
