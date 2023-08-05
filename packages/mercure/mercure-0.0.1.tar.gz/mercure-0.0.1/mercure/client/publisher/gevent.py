from gevent import spawn

from mercure.client.publisher.common import MercurePublisherClient


class MercurePublisherClientGevent(MercurePublisherClient):
    def _invoke_request(self, channel_name, event_type, event_message):
        spawn(super()._invoke_request, channel_name, event_type, event_message)
