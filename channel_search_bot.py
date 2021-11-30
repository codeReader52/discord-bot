import discord
import os


BOT_TOKEN = os.environ['BOT_TOKEN']
APPLICATION_ID = 915040872125583370

client = discord.Client()

def find_channels_matching(channels, searched_names):
    all_elligible_channels = set()
    for searched_name in searched_names:
        matching_channels = [c for c in channels if searched_name in c.name.lower()]
        all_elligible_channels.update(matching_channels)
    return all_elligible_channels

def format_channels(channels):
    return "\n".join([f'{c.name}: {c.mention}' for c in channels])

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if len(message.mentions) != 1:
        return
    
    if message.mentions[0].id != APPLICATION_ID:
        return

    content_parts = message.content.split()    

    if len(content_parts) < 3:
        await message.channel.send(f"Cannot understand command `{message.content}`")
        return
    
    command = content_parts[1] 
    searched_channel_names = [n.lower() for n in content_parts[2:]]
    
    if command != '/channels':
        await message.channel.send(f"Invalid command: {command}")
        return

    guild_id = message.guild.id
    guild_details = next(iter([g for g in client.guilds if g.id == guild_id]), None)
    if guild_details is not None:
        matching_channels = find_channels_matching(guild_details.channels, searched_channel_names)
        await message.channel.send(f"Channels: {format_channels(matching_channels)}")
    else:
        await message.channel.send(f"Can't find any guilds matching any of {searched_channel_names}")

if __name__ == "__main__":
    client.run(BOT_TOKEN)