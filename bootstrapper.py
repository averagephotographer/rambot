import discord
import os
from lock import lock
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    try:
        if message.content == ".ping":
            await message.channel.send("pong")
        if message.content == ".start "+lock():
            print("running")
            await message.channel.send("starting ram")
            await client.logout()
            print("done")
        elif message.content == ".update "+lock():
            await message.channel.send("generating backup")
            print("generating backup")
            os.system("cp ram.py rambackup.py")
            await message.channel.send("saving file")
            print("saving file")
            await message.attachments[0].save("ram.py")
        elif message.content == ".revert "+lock():
            await message.channel.send("restoring from backup")
            print("restoring from backup")
            os.system("cp rambackup.py ram.py")
        elif message.content == ".check error "+lock():
            try:
                os.system("python3 ram.py")
            except Exception as e:
                print(e)
                await message.channel.send(e)
    except Exception as e:
        print("Bootstrapper error:")
        print(e)
        await message.channel.send("Bootstrapper error: {}".format(e))


os.system("python3 ram.py")
with open('key.txt', 'r') as key:
    client.run(key.read())

    

