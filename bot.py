from enum import Enum
import discord
import configparser
import time
from urllib.request import urlretrieve
import os.path
import os

config = configparser.ConfigParser()
config.read('config.ini')
print('The token is {}'.format(config['DEFAULT']['token']))
token = config['DEFAULT']['token']
botUserId = config['DEFAULT']['userId']
vc = None
client = discord.Client()


@client.event
async def on_voice_state_update(member, beforeVs, afterVs):
    global vc
    if vc == None and member.id != int(botUserId) and member.id != 357302043532066837 and afterVs.channel != None and beforeVs.channel != afterVs.channel:
        vc = await afterVs.channel.connect()
        filename = 'Content/' + str(member.display_name) + '.wav'
        if not os.path.exists(filename):
            urlretrieve(
                'https://tetyys.com/SAPI4/SAPI4?text=Welcome%20' + member.display_name.replace(' ', '%20') + '%20to%20the%20big%20dick%20club&voice=Mike%20in%20Hall&pitch=100&speed=140', filename)
        vc.play(discord.FFmpegPCMAudio(filename),
                after=lambda e: vc.disconnect)
        while vc.is_playing():
            time.sleep(1)
        await vc.disconnect()
        time.sleep(2)
        vc = None

client.run(token)
