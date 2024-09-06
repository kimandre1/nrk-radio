import discord
from discord.ext import commands
from api import connect_bot, get_channels, select_channel, has_audio_stream

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
last_guess = {}

# FFmpeg-opsjoner for lydavspilling
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}


"""
Her bør det ryddes en god del, men jeg er alt for lat.

TO DO:
- Rydde i kommandoer
- Opprette egen commands.py fil
- errorhandling

"""

@client.event
async def on_ready():
    print("Botten er i live!")
    print("-----------------")
    
@client.command(name='kanaler', help='Lister tilgjengelige kanaler')
async def kanaler(ctx):
    await ctx.send(get_channels())


@client.command()
async def hello(ctx):
    await ctx.send("heihei :)")

@client.command(name='join', help='Botten blir med i stemmekanalen du er i')
async def join(ctx):
    if ctx.author.voice is not None:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Du må være i en kanal for at jeg skal joine.")

@client.command(name='leave', help='Botten forlater stemmekanalen')
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Slutt og mas, er da ikke her jeg!")

@client.command(name='play', help='Spiller av NRK Radio')
async def play(ctx, radio_channel: str):
    if ctx.voice_client is None:
        if ctx.author.voice is not None:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
        else:
            await ctx.send("Du må være i en stemmekanal for at botten skal kunne bli med!")
            return

    if not ctx.voice_client.is_playing():
        url = select_channel(radio_channel)
        if url:
            ctx.voice_client.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
            await ctx.send(f"Spiller av NRK Radio fra: {radio_channel}")
        else:
            await ctx.send(f'Fant ikke kanalen {radio_channel}. bruk "" før og etter kanalnavnet.')
    else:
        await ctx.send("Radioen går allerede!")

@client.command(name='stop', help='Parkerer tøflene')
async def stop(ctx):
    if ctx.voice_client is not None and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Parkert.")
    else:
        await ctx.send("Botten spiller ikke av noe for øyeblikket!")

# Legge til nye kanaler
@client.command(name="add", help='Legg til kanal, format= "kanalnavn=URL"')
async def add(ctx, channel_url: str):
    try:
        # Splitter kanalnavnet og URL-en
        channel_name, url = channel_url.split('=', 1)
        if await has_audio_stream(url.strip()):
            with open("channels.env", "a") as file:
                file.write(f"{channel_url}\n")
            await ctx.send(f"Kanalen '{channel_name.strip()}' er lagt til!")
        else:
            await ctx.send("Fant ikke kanalen med lyd.")
    except ValueError:
        await ctx.send("Formatet er feil. Bruk formatet: 'kanalnavn=URL'")

# Kjører botten med token hentet fra connect_bot-funksjonen
client.run(connect_bot())
