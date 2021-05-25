import discord
from discord.ext import tasks, commands
import datetime
import requests
import math
import os
from dotenv import load_dotenv


load_dotenv()

# Create a bot instance and sets a command prefix
client = commands.Bot(command_prefix='.', intents=discord.Intents.all())
client.remove_command('help')

@client.event
async def on_ready():
    alert.start()
    await client.get_channel(841330475742265385).send("Bot is ready")


@tasks.loop(seconds=20)
async def alert():
    #print("ping")
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    datetom = (datetime.datetime.now() +
               datetime.timedelta(days=1)).strftime("%d-%m-%Y")
    date2 = (datetime.datetime.now() +
               datetime.timedelta(days=2)).strftime("%d-%m-%Y")
    dates = [date, datetom, date2]
    d_ids = [581, 603, 604, 596]
    for j in d_ids:
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict"
        for i in dates:
            headers = {"Accept-Language": "en-IN",
                       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            data = {"district_id": j, "date": i}
            res = requests.get(url, headers=headers, params=data)
            #resp = res.json()
            #print(res.json())
            #print(res.status_code, j)
            if(res.status_code == 200):
                resp = res.json()
                for k in resp['sessions']:
                    if(len(k) != 0):
                        if(math.trunc(k['available_capacity_dose1']) >= 1 and k['min_age_limit'] == 18 and ((k['available_capacity_dose1'])-int(k['available_capacity_dose1'])) == 0):
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
                            await client.get_channel(841330475742265385).send(embed=embed)
                    else:
                        continue
            else:
                continue

client.run(os.getenv("TOKEN"))