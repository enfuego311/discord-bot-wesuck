import os
import sys
import discord
import json
import aiohttp
import asyncio
from discord.ext import commands
import random
from datetime import datetime, date, time

# discord and API tokens need to be environment variables named as below
token = os.environ.get("DISCORD_TOKEN")
tenorapi = os.environ.get("TENOR_API_KEY")
weatherapi = os.environ.get("WEATHER_API_KEY")
googleapi = os.environ.get("GOOGLE_API_KEY")

description = '''To seek and annoy'''

# set command prefix
bot = commands.Bot(command_prefix='.', description=description)

# random line function for word matching
def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

# if we see this the bot is alive
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# check if seed is set
# if not that means word of the day (wotd) isn't set so run the exception code
try: seed
except:
    wordslines = 0
    file = open(os.path.join(sys.path[0], 'words.txt'), "r")
    for line in file:
        line = line.strip("\n")
        wordslines += 1
    file.close()
    # set the seed once here to keep wotd consistent
    seed = date.today().isoformat().replace('-', '')
    random.seed(seed)
    wotdlineno = random.randrange(1, wordslines)
    f=open(os.path.join(sys.path[0], 'words.txt'))
    alllines=f.readlines()
    wotd = str.strip(alllines[int(wotdlineno)])
    # after wotd is defined reset the seed
    random.seed()
    file.close()

# set reactions to word of the day
async def wotdreact(message):
    wotd_emojis = [
    "👌",
    "😂",
    "🔥",
    "😱"
    ]
    for emoji in wotd_emojis:
        await message.add_reaction(emoji)

async def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current time
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

# top result tenor match command
# @bot.command(pass_context=True)
# async def sgif(ctx, *, search):
#     confilter = "low"
#     embed = discord.Embed(colour=discord.Colour.blue())
#     session = aiohttp.ClientSession()
#     search.replace(' ', '+')
#     response = await session.get('http://api.tenor.com/v1/search?key=' + tenorapi + '&q=' + search + '&contentfilter=' + confilter + '&limit=1&media_filter=minimal')
#     data = json.loads(await response.text())
#     embed.set_image(url=data['results'][0]['media'][0]['gif']['url'])

#     await session.close()

#     await ctx.send(embed=embed)

# random result tenor match command
# @bot.command(pass_context=True)
# async def gif(ctx, *, search):
#     confilter = "low"
#     embed = discord.Embed(colour=discord.Colour.blue())
#     session = aiohttp.ClientSession()
#     search.replace(' ', '+')
#     response = await session.get('http://api.tenor.com/v1/random?key=' + tenorapi + '&q=' + search + '&contentfilter=' + confilter + '&limit=1&media_filter=minimal')
#     data = json.loads(await response.text())
#     embed.set_image(url=data['results'][0]['media'][0]['gif']['url'])

#     await session.close()

#     await ctx.send(embed=embed)

# weather command
# @bot.command(pass_context=True)
# async def weather(ctx, *, search):
#     session = aiohttp.ClientSession()
#     session2 = aiohttp.ClientSession()
#     search.replace(' ', '+')
#     # get our latitude and longitude
#     georesp = await session.get('https://maps.googleapis.com/maps/api/geocode/json?key=' + googleapi + '&address=' + search, ssl=False)
#     geodata = json.loads(await georesp.text())
#     geolat = str(geodata['results'][0]['geometry']['location']['lat'])
#     geolon = str(geodata['results'][0]['geometry']['location']['lng'])
#     # pass the lat and lon to the weather api
#     weatheresp = await session2.get('http://api.openweathermap.org/data/2.5/weather?appid=' + weatherapi + '&lat=' + geolat + '&lon=' + geolon + '&units=imperial')
#     weatherdata = json.loads(await weatheresp.text())
#     # create the map url for the embed
#     locmapurl = 'https://maps.googleapis.com/maps/api/staticmap?center=' + \
#         geolat + ',' + geolon + '&zoom=11&size=600x200&key=' + googleapi
#     temp = str(weatherdata['main']['temp'])
#     city = weatherdata['name']
#     country = weatherdata['sys']['country']
#     cond = weatherdata['weather'][0]['description']
#     feelslike = str(weatherdata['main']['feels_like'])
#     humidity = str(weatherdata['main']['humidity'])
#     # populate the embed with returned values
#     embed = discord.Embed(title="Weather for " + city +
#                           " " + country, colour=discord.Colour.blue())
#     embed.set_image(url=locmapurl)
#     embed.add_field(name="Current Temp (Feels Like)",
#                     value=temp + "F" + " " + "(" + feelslike + "F)")
#     embed.add_field(name="Conditions", value=cond)
#     embed.add_field(name="Humidity", value=humidity + "%")
#     await session.close()
#     await session2.close()
#     await ctx.send(embed=embed)

# match various patterns including word of the day and respond with
# either random lines or react to wotd with emoji
@bot.event
async def on_message(message):
    # namestr = "marcus"
    # moviestr = "movie night"
    # herzogstr = "herzog"
    # herstr = "amanda"
    # kartstr = "kart"
    # mariostr = "mario"
    # ff2str = "ff2"
    # coolstr = "cool"
    # typongstr = "typong"
    # ffstr = "final fantasy"
    # neatostr = "neato"
    # zeldastr = "zelda"
    # timestr = "is it time"
    # timewotd = "wotd"

    # bot ignores botself
    if message.author.id == bot.user.id:
            return

#     # wotd reaction
#     if wotd in message.content.lower():
#         await wotdreact(message)

#     # other word matches with static and random line responses below
#     if namestr.lower() in message.content.lower():
#         channel = message.channel
#         await channel.send(random_line(os.path.join(sys.path[0], 'name.txt')))

#     if moviestr.lower() in message.content.lower():
#         channel = message.channel
#         await channel.send(random_line(os.path.join(sys.path[0], 'movienight.txt')))

#     if herzogstr.lower() in message.content.lower():
#         channel = message.channel
#         await channel.send(random_line(os.path.join(sys.path[0], 'herzog.txt')))
    
#     if herstr.lower() in message.content.lower():
#         channel = message.channel
#         await channel.send("At least until operation: kill wife and kids")

#     if kartstr.lower() in message.content.lower():
#         channel = message.channel
#         await channel.send("**Official We Suck Mario Kart Ranking** - 8 > SNES > 64 > 7 > Wii > GBA > DS > DD")
    
#     if mariostr.lower() in message.content.lower():
#         channel = message.channel
#         await channel.send("**Official We Suck Mario Ranking** - Odyssey > 64 > World 2 > 3 > World > 3D World > Galaxy > 1 > 2 > Galaxy 2 > Sunshine")
    
#     if ff2str.lower() in message.content.lower():
#         channel = message.channel
#         await channel.send("The thing about civilization is that we are all 72 hours away from pure cannibalistic anarchy. That clock gets reset everytime we eat, everytiem we sleep but all of life as know it are on a precipice. FF2 was about 48 hrs for me. Everything you know and care about means nothing. That's the reality of culture and civilzation. It's an absolute cosmic shadow held up by essentially nothing. Final fantasy 2 taught me that.")
    
#     if coolstr.lower() in message.content.lower():
#        channel = message.channel
#        await channel.send("cool cool cool")
    
#     if typongstr.lower() in message.content.lower():
#        channel = message.channel
#        await channel.send("Don't make fun of my typong")
    
#     if ffstr.lower() in message.content.lower():
#         channel = message.channel
#         await channel.send("**Official We Suck Final Fantasy Ranking** - FF6 > FF4 > FF7 > FF9 > FF15 > FF10 > FF12 > FF1 > FF5 > FF8 > FF3 > FF13 > FF2")

#     if neatostr.lower() in message.content.lower():
#        channel = message.channel
#        await channel.send("neato burrito")

#     if zeldastr.lower() in message.content.lower():
#        channel = message.channel
#        await channel.send("**Official We Suck Zelda Ranking** - BotW > LttP > LBW > OoT > WW > LoZ > LA > TP > MM > AoL > SS")

    # if timewotd.lower() in message.content.lower():
    #     channel = message.channel
    #     if await is_time_between(time(20,00), time(23,59)):
    #         await channel.send("The word of the day today was: **" + wotd + "**")
    #     else:
    #         await channel.send("We don't talk about the word of the day until after 8pm pacific.")

#     # this keeps us from getting stuck in this function
#     await bot.process_commands(message)



bot.run(token)
