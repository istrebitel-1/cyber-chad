import logging

from discord.ext import commands

from src.constants import GIGACHADS_GUILD_ID


logger = logging.getLogger(__name__)


@commands.group()
async def emojis_cmds(ctx: commands.Context):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"No, {ctx.subcommand_passed} does not belong to simple")


@emojis_cmds.command(
    name='r',
    aliases=['react', 'reaction']
)
async def react(
        ctx: commands.Context,
        requested_emoji: str,
        msg_id: int = None,
        guild_id: int = None,
):
    """Send reaction to message"""
    msg = ctx.message if not msg_id else await ctx.fetch_message(msg_id)
    emlist = ctx.guild.emojis if not guild_id else ctx.bot.get_guild(int(GIGACHADS_GUILD_ID)).emojis

    for emoji in emlist:
        if requested_emoji.lower() == emoji.name.lower():
            await msg.add_reaction(f'<{"a" if emoji.animated else ""}:{emoji.name}:{emoji.id}>')
            await ctx.message.delete()
            return

    await ctx.send('Что-то на эльфийском, не могу прочитать')


@emojis_cmds.command(
    name='e',
    aliases=['emoji', 'emojis']
)
async def emoji(
        ctx: commands.Context,
        requested_emoji: str,
        guild_id: int = None,
        qnt: int = 1,
):
    """Send Gigachad's club emoji"""
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


async def setup(bot: commands.bot.Bot):
    bot.add_command(emojis_cmds)
    bot.add_command(react)
    bot.add_command(emoji)
