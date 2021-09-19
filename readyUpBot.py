import discord
import os
import schedule
import time
import threading
import sqlite3
from discord.ext import commands
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

# @commands.group(invoke_without_command=True)
# def tester(ctx):
#     db = sqlite3.connect('main.sqlite')
#     cursor = db.cursor()
#     pl = cursor.execute(f"SELECT user_id FROM queue WHERE guild_id = {ctx.guild.id}").fetchall
#     myString = ""
#     for x in pl:
#         myString += "\n" + str(x)
#     return myString

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}  {bot.user.id}\nMy current prefix is: -')


@commands.group(invoke_without_command=True)
async def welcome(ctx):
    await ctx.send('Hi, you can do -h to view all commands \nFor first time setup do -channel to set the channel')

#Sets channel for bot use and also edits 
@bot.command(name = 'sc', aliases = ['setchannel'])
async def setChannel(ctx, channel:discord.TextChannel):
    try:
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, channel_id) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"Channel has been set to {channel.mention}")
            elif result is not None:
                sql = ("UPDATE main SET channel_id = ? WHERE guild_id = ?")
                val = (channel.id, ctx.guild.id)
                await ctx.send(f"Channel has been updated to {channel.mention}")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
    except(discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Missing channel (-sc #channel)")


@bot.command(name = 'sr', aliases = ['setrole'])
async def setRole(ctx, role:discord.Role):
    try:
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT role_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, role_id) VALUES(?,?)")
                val = (ctx.guild.id, role.id)
                await ctx.send(f"Role to ping has been set to {role.mention}")
            elif result is not None:
                sql = ("UPDATE main SET role_id = ? WHERE guild_id = ?")
                val = (role.id, ctx.guild.id)
                await ctx.send(f"Role has been updated to {role.mention}")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
    except(discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Missing role (-sr @role)")


#Readies players up and adds them to queue
@bot.command(name = 'r', aliases = ['ready'])
async def ready(ctx):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT role_id FROM main WHERE guild_id = {ctx.guild.id}")
    guildID = cursor.fetchone()

    # if cursor.execute(f"SELECT role_id FROM main WHERE guild_id = {ctx.guild.id}").fetchone():
    #     embed = discord.Embed(title = f"Cannot Ready", description= "User already ready", color = discord.Color.red())
    #     await ctx.send(embed=embed)
    #     cursor.close()
    #     db.close()
    #     return
        
    sql = ("INSERT INTO queue(guild_id, user_id) VALUES(?,?)")
    val = (ctx.guild.id, ctx.author.mention) 
    cursor.execute(sql, val)
    db.commit()
    playerCounter = cursor.execute(f"SELECT COUNT(user_id) FROM queue WHERE guild_id = {ctx.guild.id}").fetchone()
    playerCount = playerCounter[0]
    pl = cursor.execute(f"SELECT user_id FROM queue WHERE guild_id = {ctx.guild.id}").fetchall()
    separator = '\n'
    if playerCount == 5:
        embed = discord.Embed(title = f"(5/5) EVERYONE IS READY", description= f"get on {separator.join(map(str,pl))}", color = discord.Color.green())
        print(separator.join(map(str,pl)))
        await ctx.send(embed=embed)
        await ctx.send('<@&'+guildID[0]+'>')
        cursor.execute(f"DELETE FROM queue WHERE guild_id = {ctx.guild.id}")
        cursor.close()
        db.close()
    else:
        embed = discord.Embed(title = f"({playerCount}/5) Ready", description= f"{ctx.author.mention} has readied up!", color = discord.Color.orange())
        await ctx.send(embed=embed)
        print(playerCount)
        cursor.close()
        db.close()
    

#List all players in queue
@bot.command(name = 'l', aliases = ['list','queue','q'])
async def list(ctx):
    def playerList(ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        pl = cursor.execute(f"SELECT user_id FROM queue WHERE guild_id = {ctx.guild.id}").fetchall
        myString = ""
        for x in pl:
            myString += "\n" + str(x)
        return myString
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    if cursor.execute(f"SELECT COUNT(user_id) FROM queue WHERE guild_id = {ctx.guild.id}").fetchone():
        embed = discord.Embed(title = f"Players Ready:", description= playerList(ctx), color = discord.Color.from_rgb(73,218,189))
        await ctx.send(embed=embed)
        cursor.close()
        db.close()
    else:
        embed = discord.Embed(title = f"Players Ready:", description= "no one :c", color = discord.Color.from_rgb(73,218,189))
        await ctx.send(embed=embed)
        cursor.close()
        db.close()


#Clear Queue
@bot.command(name = 'c', aliases = ['clear'])
async def clear(ctx):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM queue WHERE guild_id = {ctx.guild.id}")
    db.commit()
    embed = discord.Embed(title = f"Queue Cleared", color = discord.Color.from_rgb(73,218,189))
    await ctx.send(embed=embed)


#Display commands
@bot.command(name = 'h', aliases = ['Commands'])
async def Commands(ctx):
    embed = discord.Embed(title = f"Commands:", 
    description= '''`-sr @role or -setrole @role`| Sets role to ping when queue is full
                    \n `-sc #channel or -setchannel #channel`| Sets channel for bot use
                    \n `-r or -ready`| Readies up 
                    \n `-l or -list`| Lists all readied players 
                    \n `-c or -clear`| Clears queue (queue auto clears 12:00 AM)''',
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

