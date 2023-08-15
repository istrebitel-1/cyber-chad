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
        return False

    return True
