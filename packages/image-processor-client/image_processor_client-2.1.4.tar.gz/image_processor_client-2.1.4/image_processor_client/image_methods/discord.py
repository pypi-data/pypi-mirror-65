from .._http import HttpImageClient


class DiscordMethods(object):
    """Base class for available discord imaging methods."""

    def __init__(self, http: HttpImageClient):
        self.http = http

    async def ss_message(
            self,
            name: str,
            message_content: str,
            avatar_url: str,
            name_color: tuple = None,
            time_stamp: str = None
    ):
        """Requests server to process screenshot of a discord message using provided parameters and returns image\
        bytes.

        Note
        ----
        For now it only supports text message content.

        Parameters
        ----------
        name : str
            Name of discord User or Member who sent the message.
        message_content : str
            Full clean message content
        avatar_url : str
            Direct avatar URL of discord User or Member who sent the message.
        name_color : tuple, optional
            A tuple representing RGB color of discord User or Message who sent the message. It's default value\
            is set to ``(255, 255, 255)``.
        time_stamp : str, optional
            String representing date and time stamp of epoch when message was sent. Uses ``Today at 11:38 AM``\
            if not provided.

        Returns
        -------
        bytes
            Binary image bytes which appears as screenshot of a discord message.

        """
        if name_color:
            name_color = list(name_color)

        kwargs = {
            "name": name,
            "message_content": message_content,
            "avatar_url": avatar_url,
            "name_color": name_color,
            "time_stamp": time_stamp
        }

        data = await self.http.ss_discord_message(**kwargs)
        return data.read_data

    async def get_welcome_banner(self, banner_url: str, avatar_url: str, name: str, text: str, **options):
        """Requests for welcome banner mostly used by discord servers to welcome newly joined members with custom text.

        Note
        ----
        It supports most of the image formats including GIFs.

        Parameters
        ----------
        banner_url: str
            Direct URL of the banner file to be used as template. It can also be a GIF.
        avatar_url: str
            Direct URL of member's avatar to be pasted on banner.
        name: str
            Discord name of new member or anything.
        text: str
            Custom text to be written after name.
        border_color: str, optional
            Specify banner border color.
        font_color: str, optional
            Specify font color for banner text.
        avatar_border_color: str, optional
            Specify border color for avatar.

        Returns
        -------
        bytes
            Binary image bytes of banner. It can also be a GIF.

        """
        kwargs = {
            "banner_url": banner_url,
            "avatar_url": avatar_url,
            "name": name,
            "text": text
        }
        kwargs.update(options)
        data = await self.http.fetch_welcome_banner(**kwargs)
        return data.read_data

    REQUIRED_PROFILE_RANK_CARD_DATA = [
        "name", "avatar_url", "discriminator", "text_rank", "voice_rank",
        "text_xp", "text_target_xp", "text_total_xp", "text_level",
        "voice_xp", "voice_target_xp", "voice_total_xp", "voice_level",
    ]

    async def get_profile_rank_card(self, **kwargs):
        """Requests to generate member's rank card bounded to every discord guild.

        Parameters
        ----------
        name : str
            Discord name of the member. Without discriminator.
        discriminator : str
            Discord discriminator of the member.
        avatar_url : str
            Direct link to member's avatar URL.
        text_rank : int
            Member's text rank in the guild.
        voice_rank : int
            Member's voice rank in the guild.
        text_xp : int
            Member's text xp.
        text_target_xp : int
            The xp needed for the next level.
        text_total_xp : int
            Total text xp of the member.
        text_level : int
            Text chat level of the member.
        voice_xp : int
            Member's voice xp.
        voice_target_xp : int
            The xp needed for next voice level.
        voice_total_xp : int
            Total voice xp of the member.
        voice_level : int
            Voice level of the member.

        Returns
        -------
        bytes
            Binary image bytes of generated rank card of the member.

        Raises
        ------
        KeyError
            Raise KeyError when any of the required data key is not present.

        """
        if not all(key in kwargs for key in self.REQUIRED_PROFILE_RANK_CARD_DATA):
            raise KeyError

        data = await self.http.fetch_profile_rank_card(**kwargs)
        return data.read_data
