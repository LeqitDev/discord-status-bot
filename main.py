import asyncio
import json

from bot import *
from quart import Quart, request

app = Quart(__name__)
intents = discord.Intents.default()
intents.message_content = True
with open('subscriber.json') as file:
    data = json.load(file)
client = MyClient(intents=intents, data=data)
with open('.env') as file:
    token = file.readline()
print(token)


@app.before_serving
async def before_serving():
    loop = asyncio.get_event_loop()
    await client.login(token)
    loop.create_task(client.connect())


@app.route('/status-update/<string:user_id>/<string:status>', methods=['GET'])
async def return_response(user_id, status):
    channel = client.get_channel(1045054271730745354)
    with open('subscriber.json') as file:
        data = json.load(file)

    # json_res = await request.get_json()

    if user_id in data:
        msgtxt = data[user_id]['msg']
        msgid = data[user_id]['msg-id']
        data[user_id]['status'] = status
        msg = await channel.fetch_message(msgid)
        await msg.edit(content=f'{msgtxt} {status}')
        return 'OK', 200


    # if f'{user_id}' in json_res and 'status' in json_res:
    #     if json_res['user-id'] in data:
    #         data[json_res['user-id']]['status'] = json_res['status']
    #         msg = await channel.fetch_message(data[json_res['user-id']]['msg-id'])
    #         await msg.edit(content=f'{data[json_res["user-id"]]["msg"]} {json_res["status"]}')
    #         return 'OK', 200
    #     return 'Error 1', 401

    return 'Error 2', 401


@app.after_serving
async def after_serving():
    with open('subscriber.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == '__main__':
    app.run()
