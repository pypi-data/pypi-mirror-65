from asyncio import create_task
from json import dumps

from aiohttp import ClientSession

from mercure.client.publisher.base import (
    DEFAULT_EVENT_TYPE_SIZE,
    DEFAULT_EVENT_MESSAGE_SIZE,
    BasePublisherClient,
)


class MercurePublisherClientAsync(BasePublisherClient):
    def __init__(self, 
                 hub_url,
                 event_type_size=DEFAULT_EVENT_TYPE_SIZE,
                 event_message_size=DEFAULT_EVENT_MESSAGE_SIZE,
                 channel_generation_salt='',
                 transport_session=None):
        super().__init__(hub_url, event_type_size, event_message_size,
                         channel_generation_salt)
        self.session = transport_session or ClientSession()

    async def _request(self, channel_name, event_type, event_message):
        message = {'event_type': event_type, 'event_message': event_message}
        try:
            await self.session.post(
                url=self.hub_url,
                params={'id': channel_name},
                data=dumps(dumps(message)),
            )
        except Exception:
            pass

    def _invoke_request(self, channel_name, event_type, event_message):
        create_task(self._request(channel_name, event_type, event_message))
