from dislash import SlashClient, ActionRow, Button
from dislash.interactions.message_components import ButtonStyle

from resources import bot


slash = SlashClient(bot)


@bot.command(
    name='p_help'
)
async def help(ctx):
    """Help command"""
    await ctx.send('Какая помощь, я podliva')


@bot.event
async def on_message(message):
    """Every eessage in channel event"""
    if message.author == bot.user:
        return

    if message.content.lower() == 'да':
        await message.channel.send('pizda')
    elif message.content.lower() == 'нет':
        await message.channel.send('pidora otvet')

    await bot.process_commands(message)


@bot.command(
    name='test',
    aliases=['kekus']
)
async def podliva_checker(ctx):
    """Podliva user detection"""
    def check_button_click(inter):
        return inter.message.id == msg.id
    row_of_buttons = ActionRow(
        Button(
            label="jopa",
            custom_id="green",
            style=ButtonStyle.green,
        ),
    )

    await ctx.message.delete()

    msg = await ctx.send("А?", components=[row_of_buttons])
    inter = await ctx.wait_for_button_click(check_button_click)

    await ctx.send(
        f'Получается, что {inter.author.mention} - подлива <a:PETTHEPEEPO:749651053288357979>'
    )
    await msg.delete()
