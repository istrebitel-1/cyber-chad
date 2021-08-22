from resources import bot
from dislash import SlashClient, ActionRow, Button
from dislash.interactions.message_components import ButtonStyle


slash = SlashClient(bot)


# help ??
@bot.command(
    name='p_help'
)
async def help(ctx):
    await ctx.send('какая помощь, я podliva')
    

# message in channel event
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == 'да':
        await message.channel.send('pizda')
    elif message.content.lower() == 'нет':
        await message.channel.send('pidora otvet')

    await bot.process_commands(message)
    

# podliva detect
@bot.command(
    name = 'test',
    aliases = ['kekus']
)
async def test(ctx):

    row_of_buttons = ActionRow(
        Button(
            label="jopa",
            custom_id="green",
            style=ButtonStyle.green
        )
    )
    
    await ctx.message.delete()
    
    msg = await ctx.send(
        "А?",
        components=[row_of_buttons]
    )

    def check(inter):
        return inter.message.id == msg.id
    inter = await ctx.wait_for_button_click(check)

    await ctx.send('Получается, что %s - подлива <a:PETTHEPEEPO:749651053288357979>' % (inter.author.mention))
    await msg.delete()
