import logging

from discord.ext import commands


logger = logging.getLogger(__name__)


async def is_author_connected_to_voice(ctx: commands.Context) -> bool:
    """Check is author connected to voice

    Args:
        ctx (commands.Context): Discord context

    Returns:
        bool: Is author connected to voice
    """

    if not ctx.author.voice:
        logger.warning(f'{ctx.author.mention} not connected to voice')

        await ctx.send(f'{ctx.author.mention} Подключись к голосовому каналу, сталкер')
        return False

    return True
