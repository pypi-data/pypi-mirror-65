import unittest
from typing import Union

from image_processor_client import Client

import asyncio


class DiscordMethodsTest(unittest.TestCase):

    SAMPLE_SS_MSG_DATA = {
        "name": "The Cosmos",
        "message_content": "Python unittests test message content.",
        "avatar_url": "https://i.imgur.com/qgATqeF.png",
    }

    SAMPLE_WELCOME_BANNER_DATA = {
        "banner_url": "https://cdn.discordapp.com/attachments/509502631849492525/548458089897000977/Banner.png",
        "avatar_url": "https://cdn.discordapp.com/avatars/331793750273687553/dccee12134542a7ffab8e243ea8cce55.webp",
        "name": "The Cosmos",
        "text": "Welcome to the Universe."
    }

    SAMPLE_PROFILE_RANK_CARD_DATA = {
            "name": "□ | The Cosmos", "discriminator": "#6811",
            "avatar_url": "http://localhost/haru.jpg", "text_rank": 7, "voice_rank": 2,
            "text_xp": 75, "text_target_xp": 100, "text_total_xp": 1291, "text_level": 11,
            "voice_xp": 60, "voice_target_xp": 100, "voice_total_xp": 170, "voice_level": 17,
        }

    @staticmethod
    def __run_async(function):
        return asyncio.get_event_loop().run_until_complete(function)

    def test_get_msg_ss(self):
        return self.__run_async(self._get_msg_ss())

    async def _get_msg_ss(self):
        client = Client("http://0.0.0.0:5000/")
        ss_bytes = await client.discord.ss_message(**self.SAMPLE_SS_MSG_DATA)
        self.assertIsInstance(ss_bytes, Union[bytes])

    def test_get_welcome_banner(self):
        return self.__run_async(self._get_welcome_banner())

    async def _get_welcome_banner(self):
        client = Client("http://0.0.0.0:5000/")
        banner_bytes = await client.discord.get_welcome_banner(**self.SAMPLE_WELCOME_BANNER_DATA)
        self.assertIsInstance(banner_bytes, Union[bytes])

    def test_union_method(self):
        return self.__run_async(self._get_profile_rank_card())

    async def _get_profile_rank_card(self):
        client = Client("http://127.0.0.1:5000")
        rank_card_bytes = await client.discord.get_profile_rank_card(**self.SAMPLE_PROFILE_RANK_CARD_DATA)
        self.assertIsInstance(rank_card_bytes, Union[bytes])
