import discord
from discord.ext import tasks, commands
import datetime
import requests
import math
import os
from dotenv import load_dotenv
#import schedule
import time
import asyncio
load_dotenv()
from app import client
# Create a bot instance and sets a command prefix
'''client = commands.Bot(command_prefix='.', intents=discord.Intents.all())
client.remove_command('help')'''
#client = discord.Client()


@client.event
async def on_ready():
    # alert.start()
    print('test')
    await client.get_channel(846785400726224976).send("Bot is ready")


'''@client.command()
async def ping(ctx):
    await ctx.send(f"Ping: {round(client.latency * 1000)}ms")'''


# @tasks.loop(seconds=30)
async def alert():
    await client.wait_until_ready()
    while True:
        print("ping")
        await client.get_channel(849518539140366427).send('Bot is pinging')
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        datetom = (datetime.datetime.now() +
                   datetime.timedelta(days=1)).strftime("%d-%m-%Y")
        date2 = (datetime.datetime.now() +
                 datetime.timedelta(days=2)).strftime("%d-%m-%Y")
        dates = [date, datetom]
        d_ids = [581, 603, 604]
        for j in d_ids:
            url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict"
            for i in dates:
                headers = {"Accept-Language": "en-IN",
                           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                data = {"district_id": j, "date": i}
                res = requests.get(url, headers=headers, params=data)
                #resp = res.json()
                # print(res.json())
                #print(res.status_code, j)
                await client.get_channel(849518539140366427).send(str(res.status_code))
                if(res.status_code == 200):
                    resp = res.json()
                    for k in resp['sessions']:
                        if(len(k) != 0):
                            if(math.trunc(k['available_capacity_dose1']) >= 8 and k['min_age_limit'] == 18 and ((k['available_capacity_dose1'])-int(k['available_capacity_dose1'])) == 0):
                                embed = discord.Embed(
                                    title=f"Vaccine Available at {k['name']}", color=discord.Color.green())
                                embed.add_field(
                                    name='Date', value=k['date'], inline=False)
                                embed.add_field(
                                    name='Address', value=k['address'], inline=False)
                                embed.add_field(
                                    name='Pincode', value=k['pincode'], inline=False)
                                embed.add_field(
                                    name='Available Capacity for Dose 1', value=k['available_capacity_dose1'], inline=False)
                                embed.add_field(
                                    name='Available Capacity for Dose 2', value=k['available_capacity_dose2'], inline=False)
                                embed.add_field(
                                    name='Minimum Age', value=k['min_age_limit'], inline=False)
                                embed.add_field(
                                    name='Vaccine', value=k['vaccine'])
                                embed.add_field(
                                    name='Fee type', value=k['fee_type'], inline=False)
                                embed.add_field(name="Slots", value='\n'.join(
                                    k['slots']), inline=False)
                                await client.get_channel(846785400726224976).send(embed=embed)
                                await client.get_channel(849518939948056597).send(embed=embed)

                        else:
                            continue
                else:

                    await client.get_channel(841330475742265385).send('Message Rohan,there is an error lol'+str(res.status_code))
                    await client.get_channel(849518539140366427).send('Message Rohan,there is an error lol'+str(res.status_code))
                    continue
        await asyncio.sleep(20)
        print('res')

client.loop.create_task(alert())
#client.run(os.getenv("TOKEN"))
'''schedule.every(10).seconds.do(alert)
while True:
    print('running')
    schedule.run_pending()
    time.sleep(1)'''
