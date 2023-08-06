from asyncio import create_task

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError

from mercure.client.publisher.base import (
    DEFAULT_EVENT_TYPE_MAX_SIZE,
    DEFAULT_EVENT_MESSAGE_MAX_SIZE,
    BasePublisherClient,
)


class MercurePublisherClientAsync(BasePublisherClient):
    def __init__(self,
                 hub_url,
                 event_type_max_size=DEFAULT_EVENT_TYPE_MAX_SIZE,
                 event_message_size=DEFAULT_EVENT_MESSAGE_MAX_SIZE,
                 channel_generation_salt='',
                 transport_session=None):
        super().__init__(hub_url, event_type_max_size, event_message_size,
                         channel_generation_salt)
        self.session = transport_session or ClientSession()

    async def _request(self, channel_name, payload):
        try:
            await self.session.post(
                url=self.hub_url,
                params={'id': channel_name},
                data=payload,
            )
        except ClientError:
            # We don't guarantee delivery, failing silently
            pass

    def _invoke_request(self, channel_name, payload):
        create_task(self._request(channel_name, payload))
