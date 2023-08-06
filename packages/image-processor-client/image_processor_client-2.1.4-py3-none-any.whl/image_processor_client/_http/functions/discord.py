from abc import ABC

from .models import ImageFunction


class DiscordFunctions(ImageFunction, ABC):

    async def ss_discord_message(self, **kwargs):
        route = self.route("/discord/ss/message/")
        data = await self.request(route, json=kwargs)
        return data

    async def fetch_welcome_banner(self, **kwargs):
        route = self.route("/discord/banners/welcome/")
        data = await self.request(route, json=kwargs)
        return data

    async def fetch_profile_rank_card(self, **kwargs):
        route = self.route("/discord/profile/rank/")
        data = await self.request(route, json=kwargs)
        return data
