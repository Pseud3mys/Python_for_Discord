import run_python_discord as PyDiscord

from discord.ext import commands

TOKEN = 'ODM5NTA2MjI3MDQxNTM0MDAz.YJKpGQ.FyPqcrdUusDd2NlCxA--r37o2v8'
PREFIX = '!'

bot = commands.Bot(command_prefix=PREFIX)

GLOBALconsole = PyDiscord.console()


@bot.command()
async def help2(ctx):
    help_page = "help ```"
    help_page += """
    !ping         - if the bot is alive the response will be "pong".
    
    !script or !s - run the following text as a Python script. 
                    The output will be send as a message.
                    
    !input or !i  - use it when a script ask for an input.
    
    !console      - toggle the console on your messages. 
                    (all your following messages will be executed as python code. 
                    except command. use "exit" to quit console)
                    
    !c {code}     - as "!console" but without toggle
    
    !clear        - clear the console."""
    help_page += "```"
    await ctx.send(help_page)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
async def script(ctx, *, content):
    _script = PyDiscord.script(ctx, content)
    await _script.run()


@bot.command()
async def s(ctx, *, content):
    _script = PyDiscord.script(ctx, content)
    await _script.run()


@bot.command()
async def input(ctx, *args):
    if args == ():
        return
    _input = args[0]
    print("GET:", _input)
    if PyDiscord.EXPECT_INPUT:
        PyDiscord.INPUTS[ctx.author] = _input
    else:
        await ctx.send("input provide but not required by a script: " + _input)


@bot.command()
async def i(ctx, *args):
    if args == ():
        return
    args = args[0]
    await input(ctx, args)


@bot.command()
async def console(ctx):
    out = GLOBALconsole.toggle_author(ctx)
    await ctx.send(out)


@bot.command()
async def c(ctx, *, content):
    await GLOBALconsole.sendANDrun(content, ctx)


@bot.command()
async def clear(ctx):
    GLOBALconsole.clear()
    await ctx.channel.send("Console Cleaned.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if GLOBALconsole.is_in_console(message.author):
        if message.content == "exit":
            out = GLOBALconsole.toggle_author(message)
            await message.channel.send(out)
        elif message.content.startswith(PREFIX):
            pass
        else:
            await GLOBALconsole.sendANDrun(message.content, message)

    await bot.process_commands(message)


bot.run(TOKEN)
