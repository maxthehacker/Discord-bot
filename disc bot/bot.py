import discord
from discord.colour import Colour
from discord.ext import commands
import asyncpraw
import youtube_dl
import random

reddit = asyncpraw.Reddit(
  client_id="put your client id here",
  client_secret="put your client secret here",
  user_agent="this can be anything",
)

description = ''' An example bot to showcase the discord.ext '''

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='?', description=description, intents=intents)




@bot.event
async def on_ready():
  print('Logged in as')
  print(bot.user.name)
  print(bot.user.id)
  print('----------')
  game = discord.Game('with your mum')
  await bot.change_presence(status=discord.Status.do_not_disturb, activity=game)

@bot.command()  
async def add(ctx, a: int, b: int):
  await ctx.send(a + b)

@bot.command()
async def choose(ctx, *choices):
  await ctx.send(random.choice(choices))

@bot.command()
async def meme(ctx):
  sub = await reddit.subreddit('memes')
  meme = await sub.random()
  print(meme)
  embed = discord.Embed(title=meme.title, colour=Colour.from_rgb(51,204,255))
  embed.set_image(url=meme.url)
  embed.set_footer(text=f"👍: {meme.score}", icon_url=meme.url) 
  await ctx.send(embed=embed)

@bot.command(description="Plays music")
async def play(ctx, *query: str): 
  query = " ".join(query)
  voiceChannel = ctx.message.author.voice.channel
  voice = discord.utils.get(bot.voice_clients, guild=ctx.message.guild)

  def makeEmbed(title, url):
    embed = discord.Embed(title="Now playing", colour=Colour.from_rgb(51,204,255))
    embed.add_field(name="song", value=title)
    embed.set_image(url=url)
    return embed
    
    

  if voice == None:
    print(ctx.message.author.voice.channel)
    voice = await voiceChannel.connect()
    with youtube_dl.YoutubeDL({}) as ydl:
      song = ydl.extract_info(f"ytsearch:{query}", download=False)
      voice.play(discord.FFmpegPCMAudio(song['entries'][0]["formats"][0]["url"]))
      embed = makeEmbed(song['entries'][0]['title'], song['entries'][0]['thumbnails'][-1]['url'])
      await ctx.send(embed=embed)
  elif voice.is_connected:
      with youtube_dl.YoutubeDL({}) as ydl:
        song = ydl.extract_info(f"ytsearch:{query}", download=False)
        voice.stop()
        voice.play(discord.FFmpegPCMAudio(song['entries'][0]["formats"][0]["url"]))
        embed = makeEmbed(song['entries'][0]['title'], song['entries'][0]['thumbnails'][-1]['url'])
        await ctx.send(embed=embed)

@bot.command()
async def stop(ctx):
  voice = discord.utils.get(bot.voice_clients, guild=ctx.message.guild)
  if voice.is_connected:
    voice.stop()
    await ctx.send("**Alright...I'll shut up**")
  else:
    await ctx.send('you are not in any channel!')

@bot.command()
async def pause(ctx):
  voice = discord.utils.get(bot.voice_clients, guild=ctx.message.guild)
  if voice.is_connected:
    voice.pause()
    await ctx.send("**Paused!**")
  else:
    await ctx.send('**you are not in any channel!**')

@bot.command()
async def resume(ctx):
  voice = discord.utils.get(bot.voice_clients, guild=ctx.message.guild)
  if voice.is_connected:
    voice.resume()
    await ctx.send("**Resumed!**")
  else:
    await ctx.send('**you are not in any channel!**')

@bot.command()
async def disconnect(ctx):
  voice = discord.utils.get(bot.voice_clients, guild=ctx.message.guild)
  if voice.is_connected:
    await voice.disconnect()
    await ctx.send("**Ight imma head out**")
  else:
    await ctx.send('**you are not in any channel!**')    

bot.run('put your bot token here')