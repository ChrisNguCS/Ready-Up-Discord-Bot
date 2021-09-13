import discord
import os
import schedule
import time
import threading
from threading import Thread
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv


load_dotenv()
bot = commands.Bot(command_prefix='-', case_Insensitive=True)
bot.config_token = os.getenv('token')


#Turns playerlist into a string to be displayed
playerlist = []
def printList():
    myString = ""
    for x in playerlist:
        myString += "\n" + str(x)
    return myString


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}  {bot.user.id}\nMy current prefix is: -')


@commands.group(invoke_without_command=True)
async def welcome(ctx):
    await ctx.send('Hi, you can do -c to view all commands \nFor first time setup do -channel to set the channel')


#Readies players up and adds them to queue
@bot.command(name = 'r', aliases = ['ready'])
async def ready(ctx):
    if ctx.author in playerlist:
        embed = discord.Embed(title = f"Cannot Ready", description= "User already ready", color = discord.Color.red())
        await ctx.send(embed=embed)
        return
        
    playerlist.append(ctx.author.mention)
    if len(playerlist) == 5:
        chonk = get(ctx.guild.roles, name= 'chonk')
        embed = discord.Embed(title = f"(5/5) EVERYONE IS READY", description= f"get on {chonk.mention}", color = discord.Color.green())
        await ctx.send(embed=embed)
        await ctx.send(chonk.mention)
    else:
        embed = discord.Embed(title = f"({len(playerlist)}/5) Ready", description= f"{ctx.author.mention} has readied up!", color = discord.Color.orange())
        await ctx.send(embed=embed)
        print (ctx.author.mention)
    

#List all players in queue
@bot.command(name = 'l', aliases = ['list','queue','q'])
async def list(ctx):
    if playerlist:
        embed = discord.Embed(title = f"Players Ready:", description= printList(), color = discord.Color.from_rgb(73,218,189))
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title = f"Players Ready:", description= "no one :c", color = discord.Color.from_rgb(73,218,189))
        await ctx.send(embed=embed)


#Clear Queue
@bot.command(name = 'c', aliases = ['clear'])
async def clear(ctx):
    playerlist.clear()
    embed = discord.Embed(title = f"Queue Cleared", color = discord.Color.from_rgb(73,218,189))
    await ctx.send(embed=embed)


#Display commands
@bot.command(name = 'h', aliases = ['Commands'])
async def Commands(ctx):
    embed = discord.Embed(title = f"Commands:", 
    description= "-r or -ready    | Readies up \n -l or -list   | Lists all readied players \n -c or -clear | Clears queue (queue clears every day at 12:00 AM", 
    color = discord.Color.from_rgb(73,218,189))
    await ctx.send(embed=embed)


def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def background_job():
    playerlist.clear()
schedule.every().day.at("23:59").do(background_job)
stop_run_continuously = run_continuously()

bot.run(bot.config_token)

