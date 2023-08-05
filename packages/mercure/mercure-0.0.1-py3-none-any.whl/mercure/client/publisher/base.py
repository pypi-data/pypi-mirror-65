from hashlib import sha256
from urllib.parse import urljoin


DEFAULT_EVENT_TYPE_SIZE = 30
DEFAULT_EVENT_MESSAGE_SIZE = 100
CHANNEL_NAME_MAX_SIZE = 200


class BasePublisherClient:
    """
    Base Mercure client class.
    
    Sub-classes must implement BasePublisherClient._invoke_request.
    """
    def __init__(
        self, 
        hub_url,
        event_type_size=DEFAULT_EVENT_TYPE_SIZE,
        event_id_size=DEFAULT_EVENT_MESSAGE_SIZE,
        channel_generation_salt='',
    ):
        self.hub_url = urljoin(hub_url, 'pub')
        self.event_type_size = event_type_size
        self.event_id_size = event_id_size
        self.channel_generation_salt = channel_generation_salt

    def get_channel_name(self, *tags):
        """
        Generate a channel name for specific set of 'tags'. 

        Tags are any number of objects that can be cast to str.
        TODO: create the channel in the hub?
        """
        # Deterministic list of tags:
        ordered_tags = sorted([
            self.channel_generation_salt, 
            *map(str, tags),
        ])
        return sha256('|'.join(ordered_tags).encode()).hexdigest()

    def _validate_message_params(self, channel_name,
                                 event_type, event_message):
        if len(event_type) > self.event_type_size:
            raise ValueError(f'"event_type" size should not exceed '
                             f'{self.event_type_size}')
        if len(event_message) > self.event_id_size:
            raise ValueError(f'"event_message" size should not exceed '
                             f'{self.event_id_size}')
        if len(channel_name) > CHANNEL_NAME_MAX_SIZE:
            raise ValueError(f'"channel_name" size should not exceed '
                             f'{CHANNEL_NAME_MAX_SIZE}')

    def _invoke_request(self, channel_name, event_type, event_message):
        raise NotImplemented

    def publish_message(self, channel_name, event_type, event_message):
        """
        Publish a message to a given channel name.

        It doesn't allow to send complicated and big messages on purpose:
        we want to avoid authentication on the hub, thus only depersonalized
        data should be transferred through it.
        Channel name could be an arbitrary string or generated one using
        MercureClient().get_channel_name().
        
        WARNING: It doesn't provide any guarantees on message delivery, thus
        will silently fail on any network errors.
        """
        self._validate_message_params(channel_name, event_type, event_message)
        self._invoke_request(channel_name, event_type, event_message)

    def publish_message_by_tags(self, tags, event_type, event_message):
        """
        Generate a channel name from tags and push a message into it.

        It doesn't allow to send complicated and big messages on purpose:
        we want to avoid authentication on the hub, thus only depersonalized
        data should be transferred through it.
        
        WARNING: It doesn't provide any guarantees on message delivery, thus
        will silently fail on any network errors.
        """
        channel_name = self.get_channel_name(*tags)
        self.publish_message(channel_name, event_type, event_message)
