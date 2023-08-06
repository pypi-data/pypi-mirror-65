from abc import ABCMeta, abstractmethod
from hashlib import sha256
from json import dumps
from urllib.parse import urljoin


DEFAULT_EVENT_TYPE_MAX_SIZE = 30
DEFAULT_EVENT_MESSAGE_MAX_SIZE = 100
CHANNEL_NAME_MAX_SIZE = 200
# This is the exact number of extra characters in the chosen message structure
# after json-serialization
PAYLOAD_SERIALIZATION_OVERHEAD = 39


class BasePublisherClient(metaclass=ABCMeta):
    """
    Base Mercure client class.
    
    Sub-classes must implement BasePublisherClient._invoke_request.
    """
    def __init__(
        self, 
        hub_url,
        event_type_max_size=DEFAULT_EVENT_TYPE_MAX_SIZE,
        event_message_max_size=DEFAULT_EVENT_MESSAGE_MAX_SIZE,
        channel_generation_salt='',
    ):
        self.hub_url = urljoin(hub_url, 'pub')
        self.channel_generation_salt = channel_generation_salt

        # These restrictions are purely artificial: they are added to
        # somewhat enforce anonymization of payload and avoiding adding
        # any auth for the service.
        self.event_type_max_size = event_type_max_size
        self.event_message_max_size = event_message_max_size

    def get_channel_name(self, *tags):
        """
        Generate a channel name for specific set of 'tags'. 

        Tags are any number of objects that can be cast to str.

        TODO: DOS is possible if attacker subscribes to lots and lots of
        channels and eats nginx's memory. To prevent this we might want
        to forbid subscribers create channels and create channel in the hub
        somewhere around channel name generation step.
        """
        # Deterministic list of tags:
        ordered_tags = sorted([
            self.channel_generation_salt, 
            *map(str, tags),
        ])
        return sha256('|'.join(ordered_tags).encode()).hexdigest()

    def _validate_params_and_prepare_payload(self, channel_name, 
                                             event_type, event_message):
        if not isinstance(channel_name, str):
            raise ValueError('"channel_name" should be a string')
        if len(channel_name) > CHANNEL_NAME_MAX_SIZE:
            raise ValueError(f'"channel_name" size should not exceed '
                             f'{CHANNEL_NAME_MAX_SIZE}')

        if not isinstance(event_type, str):
            raise ValueError('"event_type" should be a string')
        event_type_len = len(event_type)
        if event_type_len > self.event_type_max_size:
            raise ValueError(f'"event_type" size should not exceed '
                             f'{self.event_type_max_size}')

        payload = {'event_type': event_type, 'event_message': event_message}

        try:
            payload = dumps(payload)
        except TypeError:
            raise TypeError('"event_message" should be JSON serializable')

        message_size = (
            len(payload) - event_type_len - PAYLOAD_SERIALIZATION_OVERHEAD
        )

        if message_size > self.event_message_max_size:
            raise ValueError(f'"event_message" size should not exceed '
                             f'{self.event_message_max_size} in'
                             f'JSON serialized form')

        return payload

    @abstractmethod
    def _invoke_request(self, channel_name, payload):
        pass

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
        payload = self._validate_params_and_prepare_payload(
                channel_name,
                event_type,
                event_message,
        )
        self._invoke_request(channel_name, payload)

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
