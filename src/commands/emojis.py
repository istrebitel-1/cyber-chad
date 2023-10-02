import logging

from discord.ext import commands

from src.constants import GIGACHADS_GUILD_ID
from src.commands.constants import EmojisCommands


logger = logging.getLogger(__name__)


@commands.group()
async def emojis(ctx: commands.Context, /):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"No, {ctx.subcommand_passed} does not belong to simple")


@emojis.command(
    name=EmojisCommands.REACT,
    aliases=['r', 'reaction'],
)
async def react(
        ctx: commands.Context,
        requested_emoji: str,
        msg_id: int | None = None,
        guild_id: int | None = None,
        /,
) -> None:
    """Send reaction to message

    Args:
        ctx (commands.Context): Discord context
        requested_emoji (str): Emoji name
        msg_id (int | None, optional): Message_id to react. Defaults react to current.
        guild_id (int | None, optional): Guild ID to search emojis. Defaults to current.
    """
    msg = ctx.message if not msg_id else await ctx.fetch_message(msg_id)
    emlist = ctx.guild.emojis if not guild_id else ctx.bot.get_guild(GIGACHADS_GUILD_ID).emojis

    for emoji in emlist:
        if requested_emoji.lower() == emoji.name.lower():
            await msg.add_reaction(f'<{"a" if emoji.animated else ""}:{emoji.name}:{emoji.id}>')
            await ctx.message.delete()
            return None

    await ctx.send('Что-то на эльфийском, не могу прочитать')

    return None


@emojis.command(
    name=EmojisCommands.EMOJI,
    aliases=['e'],
)
async def emoji(
        ctx: commands.Context,
        requested_emoji: str,
        guild_id: int | None = None,
        qnt: int = 1,
        /,
) -> None:
    """Send GuildID or `Gigachad's club` emoji

    Args:
        ctx (commands.Context): Discord context
        requested_emoji (str): Emoji name
        guild_id (int | None, optional): Guild ID. Defaults to None.
        qnt (int, optional): _description_. Quantity of emojis in message to 1.
    """
    try:
        emlist = ctx.guild.emojis if not guild_id else ctx.bot.get_guild(guild_id).emojis

        logger.info(f'Searching {requested_emoji} in {emlist}')

        for emoji in emlist:
            if requested_emoji.lower() == emoji.name.lower():
                message = ''.join([
                    f'<{"a" if emoji.animated else ""}:{emoji.name}:{emoji.id}>'
                    for _ in range(qnt)
                ])

                await ctx.reply(message)
                return

        await ctx.send('404 эмоджи нот фаунд <:bonk:751150126046904532>')

    except Exception as e:
        logger.error(e)
        await ctx.send('Я сломався <:bonk:751150126046904532>')


def setup(bot: commands.bot.Bot) -> None:
    """Setup function for load commands module

    Args:
        bot (commands.bot.Bot): Discord bot class
    """
    bot.add_command(react)
    bot.add_command(emoji)
