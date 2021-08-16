from resources import bot
from dislash import SlashClient, ActionRow, Button
from dislash.interactions.message_components import ButtonStyle


slash = SlashClient(bot)


# help ??
@bot.command()
async def podliva_help(ctx):
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
@bot.command()
async def test(ctx):

	row_of_buttons = ActionRow(
		Button(
			label="jopa",
			custom_id="green",
			style=ButtonStyle.green
		)
	)
	# Send a message with buttons
	msg = await ctx.send(
		"А?",
		components=[row_of_buttons]
	)
	# Wait for someone to click on them

	def check(inter):
		return inter.message.id == msg.id
	inter = await ctx.wait_for_button_click(check)
	# Send what you received
	button_text = inter.clicked_button.label
	await ctx.send('Получается, что %s - подлива' % (inter.author.mention))
	await msg.delete()
