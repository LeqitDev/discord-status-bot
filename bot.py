import discord
import asyncio
import json


class MyClient(discord.Client):
    def __init__(self, data: json, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$'):
            raw_msg = message.content.removeprefix('$')
            args = raw_msg.split(' ')
            msg = args[0]
            match msg:
                case 'hello':
                    await message.channel.send('Hello!')
                    await asyncio.sleep(3.0)
                    await message.delete()
                case 'delete':
                    amount = int(args[1]) + 1
                    print(f'Deleting {amount} Messages!')
                    await message.channel.purge(limit=amount)
                case 'subscribe':
                    print("OK")
                    if message.author.id not in self.data:
                        print(self.data)
                        channel = self.get_channel(1045054271730745354)
                        stat_msg = await channel.send('00')
                        self.data[message.author.id] = {'status': 'unknown', 'msg': raw_msg.removeprefix('subscribe '), 'msg-id': stat_msg.id, }
                        await stat_msg.edit(content=f'{raw_msg.removeprefix("subscribe ")} unknown')
                        await message.author.send('Dein Webhook: http://bot.cc-web.cloud/status-update\nMit dem folgenden '
                                            'Body: {"user-id": "%i", "status": "(Neuer Status)"}' % message.author.id)
                        with open('subscriber.json', 'w') as outfile:
                            json.dump(self.data, outfile)
                        ret_msg = \
                            await message.channel.send(f'Dich, {message.author.name}, hab ich jetzt auch im Sack!')
                        print("OK1")
                    else:
                        ret_msg = await message.channel.send(f'Dich, {message.author.name}, hab ich doch schon!')
                        print("OK2")
                    print("OK3")
                    await asyncio.sleep(3.0)
                    await message.delete()
                    await ret_msg.delete()
                case 'stop':
                    print('------')
                    print('Logged out')
                    await self.close()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


def main():
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run('ODI0NjYxNjMyODA2NDIwNTYw.GmMC5f.2-smjJh3GCJ2iBi8VcK2jwr2LQJ9OoJRFpStG0')
