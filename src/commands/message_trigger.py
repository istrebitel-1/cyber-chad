import discord
from discord.ui import View
from discord.ext import commands


class PodlivaView(View):
    @discord.ui.button(
        custom_id='podliva_button',
        label='WOW!',
        style=discord.ButtonStyle.green,
    )
    async def button_callback(self, interaction: discord.Interaction, button):
        await interaction.response.send_message(
            f'Получается, что {interaction.user.mention} - подлива <a:PETTHEPEEPO:749651053288357979>',
            # view=hihik_view,
        )
        await interaction.message.delete()


@commands.group()
async def message_trigger(ctx: commands.Context):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"No, {ctx.subcommand_passed} does not belong to simple")


@message_trigger.command(
    name='p_help',
)
async def help(ctx: commands.Context):
    """Help command"""
    await ctx.send('Какая помощь, я podliva')


@message_trigger.command(
    name='test',
    aliases=['kekus'],
)
async def podliva_checker(ctx: commands.Context):
    """Podliva user detection"""
    await ctx.message.delete()
    await ctx.send("А?", view=PodlivaView())


async def setup(bot: commands.bot.Bot):
    bot.add_command(help)
    bot.add_command(podliva_checker)
    bot.add_command(message_trigger)
