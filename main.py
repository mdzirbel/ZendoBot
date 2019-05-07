#!/usr/bin/python3.6

# Docs: https://discordpy.readthedocs.io/en/latest/api.html

# TODO make overview command

import string, random, copy, discord
from Saving import saving, logs
from discord.ext.commands import Bot
from Rule.rule import *

RANDOM_KEY_LENGTH = 10

current_rules = {}
for server_id, rule in saving.get_saved_rules().items():
    current_rules[server_id] = build_rule(rule)

BOT_PREFIX = ("?", "!")
with open("Saved/token.txt") as f:
    TOKEN = str(f.readline())

bot = Bot(command_prefix=BOT_PREFIX)

@bot.command(name='setrule',
                description="Sets the current rule in the given chat",
                brief="Sets the current rule in the given chat",
                aliases=['new rule', 'new-rule', 'new_rule', 'newrule', 'set rule', 'set-rule', 'set_rule', 'set'],
                pass_context=True)
async def set_rule(context, *, new_rule:str): # the * makes new_rule be all the following text, not just until the next space

    current_channel_id = str(context.channel.id)

    try:
        # new_rule is the raw, new_rule_to_add is the actual rule regardless

        if saving.has_rule_reference(new_rule):
            new_rule_to_add = saving.get_rule_reference(new_rule)
            setting_with_key = True
        else:
            new_rule_to_add = new_rule
            setting_with_key = False

        logs.log("Setting new rule " + new_rule_to_add + " in channel " + current_channel_id + " " + context.channel.name + " for " + str(context.message.author))

        current_rules[current_channel_id] = build_rule(new_rule_to_add, verbose=False)
        saving.save_rule(context.channel.id, new_rule_to_add)

        saving.clear_checked_guesses(current_channel_id)

        if setting_with_key:
            await context.send("Rule set by " + context.message.author.mention + " using key: \"" + new_rule + "\"")
        else:
            await context.send("Rule set by " + context.message.author.mention + " as: `" + new_rule + "`")

    except Exception as e:
        to_send = "A problem occurred while parsing the rule. Here is the error:\n" + str(e)
        await context.send(to_send)

@bot.command(name='makekey',
                description="Gives a random key which can be used to set the rule",
                brief="Gives a random key which can be used to set the rule",
                aliases=['key', 'getkey', 'get_key'],
                pass_context=True)
async def make_key(context, *, new_rule:str): # the * makes new_rule be all the following text, not just until the next space

    try:
        build_rule(new_rule) # This doesn't do anything but ensure that it can be parsed without throwing an error

        random_key = ""
        for _ in range(RANDOM_KEY_LENGTH):
            random_key += random.choice(string.ascii_uppercase)

        saving.save_rule_reference(random_key, new_rule)

        logs.log("Making key " + random_key + " for rule " + new_rule + " for " + str(context.message.author))

        await context.send("Made key "+random_key+" for the rule. Use this key in any channel to set the rule there.")

    except Exception as e:
        to_send = "A problem occurred while parsing the rule. Here is the error:\n" + str(e)
        await context.send(to_send)

@bot.command(name='check',
                description="Checks whether the guess fits the rule",
                brief="Checks whether the guess fits the rule",
                aliases=['checkguess', 'check-guess', 'master', 'try', 't'],
                pass_context=True)
async def check_guess(context, *, guess:str): # the * makes new_rule be all the following text, not just until the next space

    current_channel_id = str(context.channel.id)

    logs.log("Checking guess " + guess + " in channel " + current_channel_id + " " + context.channel.name)

    if current_channel_id in current_rules:
        try:
            result = current_rules[current_channel_id].evaluate_top_level(guess, verbose=False)

            saving.save_checked_guess(current_channel_id, guess, result)

            p_lazy = .01 # Chance to respond 'Ehhh probably' or 'I doubt it'

            if result:
                if random.random() < p_lazy:
                    await context.send("Ehhh probably")
                else:
                    await context.send(guess + " fits the rule")
            else:
                if random.random() < p_lazy:
                    await context.send("I doubt it")
                else:
                    await context.send(guess + " does not fit the rule")

        except Exception as e:
            to_send = "A problem occurred while interpreting the guess. Here is the error:\n" + str(e)
            await context.send(to_send)

    else:
        await context.send("There is no rule currently set in this chat")


@bot.command(name='overview',
             description="Gives results for all already tried guesses",
             brief="Gives results for all already tried guesses",
             aliases=['past', 'o', 'past-guesses', 'pastguesses', 'history'],
             pass_context=True)
async def get_overview(context):  # the * makes new_rule be all the following text, not just until the next space

    max_guesses_to_show = 30

    current_channel_id = str(context.channel.id)

    logs.log("Retrieving overview in channel " + current_channel_id + " " + context.channel.name)

    past_guesses = saving.get_checked_guesses(current_channel_id)

    if past_guesses: # If it's not empty

        to_reply = "Showing " + str(min(len(past_guesses), max_guesses_to_show)) + " of " + str(len(past_guesses)) + " guesses:\n"

        for guess, result in past_guesses[:max_guesses_to_show]:
            if result:
                to_reply += "Passed: " + guess + "\n"
            else:
                to_reply += "Failed: " + guess + "\n"

        to_reply = to_reply.strip() # Remove the trailing newline

        await context.send(to_reply)

    else:

        await context.send("No previous guesses to show")


@bot.command(name='clearchat',
                description="Deletes num messages in the current chat",
                brief="Deletes num messages in the current chat",
                aliases=['clear', 'clear chat', 'clear_chat', 'clear-chat', 'cls'],
                pass_context=True)
async def clear_chat(context, number):
    if str(context.message.author) == "mdzirbel#7290":
        print("Deleting",number,"messages for",context.message.author)
        logs.log("Deleting " + str(number) + " messages for " + str(context.message.author) + "\n")
        try:
            number = int(number)  # Converting the amount of messages to delete to an integer
            async for msg in context.history(limit=number):
                await msg.delete()
        except TypeError: # Expected when number is not an int
            pass

@bot.command(name='id',
                description="Sends the current channel id",
                brief="Sends the current channel id",
                aliases=['channel_info', 'channel_id'],
                pass_context=True)
async def channel_id(context):

    current_channel = str(context.channel.id)

    await context.send("Current channel id: " + current_channel)

@bot.command(name='getrule',
             description="Sends the current channel id",
             brief="Sends the current channel id",
             aliases=['get_rule'],
             pass_context=True)
async def get_rule(context):  # the * makes new_rule be all the following text, not just until the next space


    if str(context.message.author) == "mdzirbel#7290":

        current_channel = str(context.channel.id)

        current_rules[str(current_channel)].print()

        # await context.send("Rule:" + current_rules[current_channel])

    else:
        await context.send("Nice try")

@bot.event
async def on_member_join(member):
    await make_private_channel(member.guild, member)

@bot.event
async def on_ready():
    await bot.change_presence()
    print("Logged in as " + bot.user.name)

    for guild in bot.guilds:
        for member in guild.members:
            if member.name != "Text-Zendo Bot":
                has_private_channel = False # Whether they already have a private channel
                for channel in guild.text_channels:
                    if channel.name == "private-work-area":
                        if member in channel.members:
                            has_private_channel = True
                if not has_private_channel:
                    await make_private_channel(guild, member)

@bot.command(name='exit',
                description="Stops Text-Zendo bot",
                brief="Stops Text-Zendo bot",
                aliases=['quit', 'stop', 'e'],
                pass_context=False)
async def stop():
    print("Stopping by discord stop command")
    await bot.logout()

async def make_private_channel(guild, user, verbose=True):
    if verbose: print("Making private channel for", user)
    logs.log("Making private work area for " + ''.join(e for e in user.name if e.isalnum()))

    name = "private-work-area"
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.owner: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        user: discord.PermissionOverwrite(read_messages=True)
    }
    category = None
    for channel in guild.text_channels:
        if channel.name == "Zendo":
            category = channel
    topic = "Create and test rules, then create the key for them and set them as the rule in other channels"
    reason = str(user.name)

    new_channel = await guild.create_text_channel(name, overwrites=overwrites, category=category, topic=topic, reason=reason)

    await new_channel.send("This is a workspace where you can privately create and test rules. You can also generate keys for rules privately "
                           "and use them in other channels")

bot.run(TOKEN)