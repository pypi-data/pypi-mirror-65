from random import shuffle
from unittest import TestCase

from mercure.client.publisher.base import BasePublisherClient


class BasePublisherClientTestCase(TestCase):
    def setUp(self):
        self.client = BasePublisherClient(hub_url='http://localhost',
                                          channel_generation_salt='yammy')
    
    def test_get_channel_name(self):
        expected = (
            '73d6cd526857b9a0c9f7e3d9b7eed5db730b13a14e6f889081064019f5ccc17c'
        )

        tags = ['any', 1, 'of', 'objs']
        channel_name = self.client.get_channel_name(*tags)
        self.assertEqual(
            channel_name,
            expected,
        )

        shuffle(tags)
        # check that any order gives same result
        channel_name = self.client.get_channel_name(*tags)
        self.assertEqual(
            channel_name,
            expected,
        )
