#schedule.every().day.at("13:10").do(clear())

#Run scheduler so that everyday at 12:00 AM the playerlist is cleared
# def scheduler():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# def run_continuously(interval=1):
#     cease_continuous_run = threading.Event()

#     class ScheduleThread(threading.Thread):
#         @classmethod
#         def run(cls):
#             while not cease_continuous_run.is_set():
#                 schedule.run_pending()
#                 time.sleep(interval)

#     continuous_thread = ScheduleThread()
#     continuous_thread.start()
#     return cease_continuous_run


# async def background_job(ctx):
#     playerlist.clear()
#     embed = discord.Embed(title = f"Queue Cleared")
#     await ctx.send(embed=embed)


# schedule.every().second.do(background_job)

# # Start the background thread
# stop_run_continuously = run_continuously()
# @bot.command(pass_context=True)
# @tasks.loop(seconds=5)
# async def scheduleClear(ctx):
#     await clear(ctx)

#t1 = threading.Thread(target=scheduler, name='t1')
#t1.start()