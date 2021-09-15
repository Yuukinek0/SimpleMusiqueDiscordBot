#Install companent with this line in cmd windows :
#py -3 -m pip install pynacl
#py -3 -m pip install youtube_dl

#With windows install ffmpeg
#This link is in french but its easy to use and understand :
#https://youtu.be/tPi3PQWP3sc

#For mac and linux use this in your terminal
#python3 -m pip install pynacl
#python3 -m pip install youtube_dl

#Credit to this guys who help me for make this simple code
#Youtube channel link : https://www.youtube.com/channel/UChDVo_Uqomuk7KnMVp-Lhhw

#I Make this bot be cause Rip all bot attacked by Youtube

#Just Dont to forget to put your bot token down

import discord, os

from discord import Embed
from discord.ext import commands

import youtube_dl, asyncio

from discord import Embed
from discord.ext import commands, tasks
from discord.utils import get

musics = {}
ytdl = youtube_dl.YoutubeDL()

list_track = []

prefix = "" #Put prefix here

bot = commands.Bot(command_prefix=prefix, help_command=None)


class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]


def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url,
                                                                 before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            self.play_song(client, queue, new_song)
            del list_track[0]
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)
            list_track.clear()

    client.play(source, after=next)

@bot.command()
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []
    list_track.clear()

@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()

@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()

@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()

@bot.command()
async def play(ctx, url):
    print("play")
    client = ctx.guild.voice_client

    # Si le bot est déjà dans un salon voc
    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
        await ctx.send("Je ajoute votre musique a la list !")
        list_track.append(url)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"I play your Song")
        play_song(client, musics[ctx.guild], video)
        list_track.append(url)

@bot.command(name="tracklist")
async def track_list(ctx):
    client = ctx.guild.voice_client
    if not list_track:
        await ctx.send("I dont have song in queue")
    else:
        embed = Embed(title="Song Queue", colour=ctx.author.colour)
        embed.add_field(name="Song Queue", value=list_track, inline=False)
        await ctx.send(embed=embed)

bot.run("") #Put Token bot here
