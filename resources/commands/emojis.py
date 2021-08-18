from resources import bot


# reaction
@bot.command(
	name='r'
)
async def react(ctx, arg, msg_id=None, guild_id=None):

	msg = ctx.message if msg_id == None else await ctx.fetch_message(msg_id)
	
	if guild_id == None:
		emlist = ctx.guild.emojis
	else:
		emlist = bot.get_guild(int(guild_id)).emojis
	
	for emoji in emlist:

		if arg.lower() == emoji.name.lower() and emoji.animated == True:

			await msg.add_reaction('<a:%s:%i>' % (emoji.name, emoji.id))
			break

		elif arg.lower() == emoji.name.lower():

			await msg.add_reaction('<:%s:%i>' % (emoji.name, emoji.id))
			break

	await ctx.message.delete()


# send Gigachad emoji
@bot.command(
	name='e',
	aliases = ['emoji', 'emojis']
)
async def emojis(ctx, arg, qnt=None, guild_id=None):

	try:
		qnt = 1 if qnt == None else int(qnt)

		flg = False

		if guild_id == None:
			emlist = ctx.guild.emojis
		else:
			guild = bot.get_guild(int(guild_id))
			print(guild)
			emlist = guild.emojis

		for emoji in emlist:

			if arg.lower() == emoji.name.lower() and emoji.animated == True:
				
				msg_text = ''

				while int(qnt) != 0:
					msg_text += '<a:%s:%i>' % (emoji.name, emoji.id)
					qnt -= 1

				await ctx.reply(msg_text)
				flg = True

				break

			elif arg.lower() == emoji.name.lower():
				
				msg_text = ''
				
				while int(qnt) != 0:
					msg_text += '<:%s:%i>' % (emoji.name, emoji.id)
					qnt -= 1

				await ctx.reply(msg_text)
				flg = True

				break

		if flg == False:
			await ctx.send('Что-то на эльфийском, не могу прочитать')

	except Exception as e:
		print(e)
		await ctx.send('Многа букаф <:bonk:751150126046904532>')
