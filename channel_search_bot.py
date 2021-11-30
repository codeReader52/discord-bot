import discord
import os


BOT_TOKEN = os.environ['BOT_TOKEN']

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
    
    clean_content = message.clean_content.strip()

    if not clean_content.startswith('@channel_search '):
        return

    content_parts = clean_content.split()    

    if len(content_parts) < 2:
        await message.channel.send(f"Yeah... I'm going to need a channel name to search. Try something like `@channel_search test`")
        return
    
    searched_channel_names = [n.lower() for n in content_parts[1:]]

    guild_id = message.guild.id
    guild_details = next(iter([g for g in client.guilds if g.id == guild_id]), None)

    if guild_details is None:
        await message.channel.send(f"Can't find any guilds matching any of {searched_channel_names}")

    matching_channels = find_channels_matching(guild_details.channels, searched_channel_names)
    if len(matching_channels) == 0:
        await message.channel.send(f"No such channels matching {searched_channel_names}")
    else:
        await message.channel.send(f"Channels: \n{format_channels(matching_channels)}")

        
if __name__ == "__main__":
    client.run(BOT_TOKEN)