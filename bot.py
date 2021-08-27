from enum import Enum
import discord
import configparser
import time
from urllib.request import urlretrieve
import os.path
import os
from datetime import datetime, timedelta

config = configparser.ConfigParser()
config.read('config.ini')
print('The token is {}'.format(config['DEFAULT']['token']))
token = config['DEFAULT']['token']
botUserId = config['DEFAULT']['userId']
channel = None
vc = None
client = discord.Client()

# Setting default cooldown to 60 secs. Maybe move to config file
defaultCooldownInSecs = 60
# Set up map. memberId is key, value is last timestamp the bot introduced the user
userCooldowns = {}


def check_user_cooldown_and_update(member):
    key = member.id
    currentTime = datetime.now()
    if key in userCooldowns:
        if currentTime - timedelta(seconds=defaultCooldownInSecs) > userCooldowns[key]:
            userCooldowns[key] = currentTime
            return True
        else:
            return False
    else:
        userCooldowns[key] = currentTime
        return True


@client.event
async def on_voice_state_update(member, beforeVs, afterVs):
    global vc
    global channel
    while vc != None and vc.is_playing():
        time.sleep(1)
    if (member.id != int(botUserId)
        and member.id != 357302043532066837 and afterVs.channel != None
        and beforeVs.channel != afterVs.channel
            and check_user_cooldown_and_update(member)):
        if channel != None and channel.id != afterVs.channel.id:
            await vc.disconnect()
            time.sleep(.5)
            channel = afterVs.channel
            vc = await channel.connect()
        elif channel == None or channel.id != afterVs.channel.id:
            channel = afterVs.channel
            vc = await channel.connect()
        filename = 'Content/' + str(member.display_name) + '.wav'
        if not os.path.exists(filename):
            urlretrieve(
                'https://tetyys.com/SAPI4/SAPI4?text=Welcome%20' + member.display_name.replace(' ', '%20') + '%20to%20the%20big%20dick%20club&voice=Mike%20in%20Hall&pitch=100&speed=140', filename)
        vc.play(discord.FFmpegPCMAudio(filename),
                after=lambda e: vc.disconnect)


client.run(token)
