import discord, asyncio, aiohttp, json
from discord.ext import commands

bot = commands.Bot(command_prefix=['!'], description='AutoSelfBot', self_bot=True, fetch_offline_members=False)

for cog in ['cogs.misc']:
	bot.load_extension(cog)

async def getToken():
	async with aiohttp.ClientSession() as session:
		async with session.ws_connect('ws://127.0.0.1:6463/?v=1&encoding=json', headers={'origin': 'https://discord.com'}, max_msg_size=0) as discordWS:
			await discordWS.send_str(json.dumps({'cmd': 'SUBSCRIBE', 'args': {}, 'evt': 'OVERLAY', 'nonce': 1}))
			await discordWS.send_str(json.dumps({'cmd': 'OVERLAY', 'args': {'type': 'CONNECT', 'pid': 0}, 'nonce': 1}))
			async for message in discordWS:
				messageJSON = message.json()
				try: return messageJSON['data']['payloads'][0]['token']
				except: continue

@bot.event
async def on_ready():
	print(f'Successfully grabbed the token of {bot.user.name} and bot has been loaded!')

@bot.command()
async def load(ctx, cog:str):
	try:
		bot.load_extension(cog)
		await ctx.send(f"Cog '{cog}' has been loaded.")
	except Exception as e: await ctx.send(e)

@bot.command()
async def unload(ctx, cog:str):
	try:
		bot.unload_extension(cog)
		await ctx.send(f"Cog '{cog}' has been unloaded.")
	except Exception as e: await ctx.send(e)

@bot.command()
async def reload(ctx, cog:str):
	try:
		bot.reload_extension(cog)
		await ctx.send(f"Cog '{cog}' has been reloaded.")
	except Exception as e: await ctx.send(e)

bot.run(asyncio.get_event_loop().run_until_complete(getToken()), bot=False)