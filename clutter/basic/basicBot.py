import discord

client = discord.Client()

@client.event
async def on_ready():
    print('logged in as {0.uset}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send("Hello!")

with open("key.txt",'r') as key:
    token = key.read()
print(token)
client.run(token)
