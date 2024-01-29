import discord
from discord.ui import View
from discord.ext import commands

from src.commands.constants import TextChannelCommands


class PodlivaView(View):
    @discord.ui.button(
        custom_id='podliva_button',
        label='WOW!',
        style=discord.ButtonStyle.green,
    )
    async def button_callback(self, button: discord.Button, interaction: discord.Interaction, /):
        user_mention = interaction.user.mention if interaction.user else '@everyone'

        await interaction.response.send_message(
            f'Получается, что {user_mention} - подлива <a:PETTHEPEEPO:749651053288357979>',
        )
        await interaction.message.delete()


@commands.group(name='text_channel')
async def text_channel(ctx: commands.Context, /):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"No, {ctx.subcommand_passed} does not belong to simple")


@text_channel.command(
    name=TextChannelCommands.TRAP,
    aliases=['test'],
)
async def podliva_checker(ctx: commands.Context, /):
    """Podliva user detection"""
    await ctx.message.delete()
    await ctx.send("А?", view=PodlivaView())


def setup(bot: commands.bot.Bot) -> None:
    """Setup function for load commands module

    Args:
        bot (commands.bot.Bot): Discord bot class
    """
    bot.add_command(podliva_checker)
