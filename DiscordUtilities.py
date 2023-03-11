from Database import database_connection

async def get_channel(ctx, client, channel_type, channel_name):
    if channel_type == "voice":
        for channel in ctx.guild.voice_channels:
            print(channel.id and channel.name)
            if channel.name == channel_name:
                channel_to_check = client.get_channel(channel.id)
                members = channel_to_check.members
                for member in members:
                    print(member)
                return channel.name

    elif channel_type == "text":
        for channel in ctx.guild.text_channels:
            print(channel.id and channel.name)
            if channel.name == channel_name:
                channel_to_check = client.get_channel(channel.id)
                members = channel_to_check.members
                for member in members:
                    print(member)
                return channel
