#!/usr/bin/env python3
from discord.ext import commands
import discord
import random
import os
import argparse

# Parse token from CLI argument
parser = argparse.ArgumentParser()
parser.add_argument('--token', '-t', help='Discord API Token')
args = parser.parse_args()
botToken = args.token

bot = commands.Bot(command_prefix='$')

# Make sure temp folder exists
try:
    os.mkdir("temp")
except:
    pass

# --- MEM ---
@bot.command(brief="Generator memów typu górny podpis + dolny podpis")
async def mem(ctx, podpis_gorny: str="", podpis_dolny: str="", url_obrazka: str=""):
    import python_memes.memlib
    import urllib.request

    podpis_dolny = podpis_dolny.upper()
    podpis_gorny = podpis_gorny.upper()

    imgpath = os.path.join("temp", str(ctx.message.id))
    if url_obrazka:
        urllib.request.urlretrieve(url_obrazka, imgpath)
    else:
        await ctx.message.attachments[0].save(imgpath)

    mem = python_memes.memlib.Mem()
    mem.load_image(imgpath)
    mem.add_caption(top_text=podpis_gorny, bottom_text=podpis_dolny)
    mem.save_image(imgpath + ".jpg")

    await ctx.send(file=discord.File(imgpath + ".jpg"))

    os.remove(imgpath)
    os.remove(imgpath + ".jpg")

@mem.error
async def mem_error(ctx, error):
    await ctx.send_help(mem) 
    os.remove(os.path.join("temp", str(ctx.message.id)))
    os.remove(os.path.join("temp", str(ctx.message.id) + ".jpg"))
    raise(error)



# --- DRAKE ---
@bot.command(brief="Generator memów typu Drakepost")
async def drake(ctx, podpis_gorny: str="", podpis_dolny: str=""):
    if podpis_gorny and podpis_dolny:
        import python_memes.memlib

        podpis_dolny = podpis_dolny.upper()
        podpis_gorny = podpis_gorny.upper()

        outputpath = os.path.join("temp", str(ctx.message.id) + ".jpg")

        mem = python_memes.memlib.Mem()
        mem.make_drake(top_text=podpis_gorny, bottom_text=podpis_dolny)
        mem.save_image(outputpath)

        await ctx.send(file=discord.File(outputpath))
        os.remove(outputpath)
    else:
        await ctx.send_help(drake)

@drake.error
async def drake_error(ctx, error):
    await ctx.send_help(drake) 
    os.remove(os.path.join("temp", str(ctx.message.id)))
    os.remove(os.path.join("temp", str(ctx.message.id) + ".jpg"))
    raise(error)



# --- EXPANDING BRAIN ---
@bot.command(brief="Generator memów typu expanding brain (max 6 podpisów)")
async def brain(ctx, *args):
    if len(args) < 1:
        raise Exception("You can't make image with 0 args")

    import python_memes.memlib

    outputpath = os.path.join("temp", str(ctx.message.id) + ".jpg")

    # Make list of strings and upper them
    strings = []
    for string in args:
        strings.append(str(string).upper())

    mem = python_memes.memlib.Mem()
    mem.make_expanding_brain(strings)
    mem.save_image(outputpath)

    await ctx.send(file=discord.File(outputpath))
    os.remove(outputpath)

@brain.error
async def brain_error(ctx, error):
    os.remove(os.path.join("temp", str(ctx.message.id) + ".jpg"))
    await ctx.send_help(brain)
    raise(error)



# --- D(ICE) ---
@bot.command(brief="Rzut kością o X ścianach")
async def d(ctx, max_roll: int=6):
    val = random.randint(1, max_roll)
    message = str(ctx.message.author.mention) + " wyrzucił(a) " + str(val)
    if val == 69:
        message += " Nice! ( ͡° ͜ʖ ͡°)"
    embed = discord.Embed(
            title = "Rzut kością (D" + str(max_roll) + ")",
            description = message,
            color = discord.Colour(0x2277FF)
            )

    await ctx.send(embed=embed)

@d.error
async def d_error(ctx, error):
    await ctx.send_help(d)
    raise(error)



# --- ROLL ---
@bot.command(brief="Losowa liczba od X do Y")
async def rng(ctx, min_val: int=1, max_val: int=100):
    val = random.randint(min_val, max_val)
    message = str(ctx.message.author.mention) + " wylosował(a) " + str(val)
    if val == 69:
        message += " Nice! ( ͡° ͜ʖ ͡°)"
    embed = discord.Embed(
            title = "Losowanie liczby",
            description = message,
            color = discord.Colour(0x2277AA)
            )
    await ctx.send(embed=embed)

@rng.error
async def rng_error(ctx, error):
    await ctx.send_help(rng)
    raise(error)



# --- ZW ---
@bot.command(brief="Przepowiednia, na ile ktoś tak na prawdę poszedł AFK")
async def zw(ctx, kto: str, na_ile: float=5):
    if na_ile > 99999:
        message = "Nie no, nie przesadzaj z tą liczbą minut, bo się Python spoci..."
    elif na_ile < 0:
        message = "Tak... " + kto + " cofnął się w czasie, dostał w dupę, leciał w powietrzu obrócił się i dał ci heada...\nCzas musi byc dodatni..."
    elif na_ile < 1:
        message = "Myślisz, że jesteś sprytny, co?"
    else:
        confirmedTexts = ("Potwierdzone info!", "No to nieźle!", "Nie jest to jednak do końca pewne.", "Ciekawe co robi?")
        confirmedText = confirmedTexts[random.randint(0, len(confirmedTexts)-1)]
        if kto == "<@!278554348336840714>":
            na_ile *= 4
        los = random.uniform(0.8,4)
        na_ile = int(na_ile * los)
        message = kto + " poszedł na zw na " + str(na_ile) + " minut. " + confirmedText
    embed = discord.Embed(
            title = "Przepowiednia gotowa",
            color = discord.Colour(0xFF0000),
            description = message
            )
    await ctx.send(embed=embed)

@zw.error
async def zw_error(ctx, error):
    await ctx.send_help(zw)
    raise(error)



@bot.event
async def on_ready():
    game = discord.Game(name="Minecraft")
    await bot.change_presence(activity=game)
    print('Zalogowano pomyślnie jako {0.user}'.format(bot))

bot.run(botToken)
