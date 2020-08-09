import os
import asyncio
import random
from discord.ext import commands
from dotenv import load_dotenv
import discord
import Database as serverdb
import pics
import gamemanager as gm
import connect4AI as cAI


#I can still optimize the bot for error handling like checking the channel in which the command was invoked
#The Connect4 game is not optimized because I can use bitmaps for the boards instead of 2d array, TODO :)
#May look like a mess and I need to refreactor everything but it works great.

######################################################
#INIT important stuff for the bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
RULES = os.getenv('RULES')
COMMANDS = os.getenv('COMMANDS')
rules = ""
######################################################

######################################################
#INIT stuff for the lfg commands
lfg_lst = {}
lfg_lst = []

lfg_role_id = 718395960849334332
group_valorant = []
######################################################

######################################################
#INIT stuff for valorant
agents = [
    'jett',
    'sage',
    'breach',
    'viper',
    'cypher',
    'reyna',
    'brimstone',
    'raze',
    'pheonix',
    'omen',
    'sova'
]
######################################################

#INIT the bot
bot = commands.Bot(command_prefix='!')

#--------------------------------------------------------------------------------------#
#Helper functions block
######################################################
#Background task test
async def test_bg_task():
    await bot.wait_until_ready()
    print(f'Started bg task')
    users = server.members
    while not bot.is_closed():
        print(f'10 Mins passed, looking')
        for user in users:
            for role in user.roles:
                flag = False
                if role == rankUpRole:
                    break
                if role in valorant_roles.values():
                    flag = True
            if flag:
                await addUserRolePoint(user.id)
                print(f'{user} got a point')
        
        await asyncio.sleep(600)
######################################################

######################################################
#INIT rules and commands for printing them in the appropriate channel
def getRules(filename):
    f = open(filename, 'r')
    global rules
    rules = f.read()
    f.close()

def getCommands(filename):
    f = open(filename, 'r')
    global commands
    commands = f.read()
    f.close()

#Checks if the rule message is the same as the bot
def check_channel_rules(m):
    return m.author == bot.user
######################################################

######################################################
#INIT all the vars need
def initChannels(guild):
    global guild_channels
    guild_channels = {}
    for channel in guild.channels:
        if not isinstance(channel, discord.CategoryChannel):
            guild_channels[channel.id] = channel

def initGameVoiceChannelValorant():
    global game_voice_channels_valorant
    game_voice_channels_valorant = []
    for channel in guild_channels.values():
        if 'valorant' in str(channel).lower():
            game_voice_channels_valorant.append(channel)

async def initRulesChannel(id):
    channel = guild_channels[id]
    await channel.purge(limit = 100, check= check_channel_rules)
    message = await channel.send(rules)
    await message.add_reaction(emoji = '👍')

def initLFGRole(guild):
    global lfg_role
    lfg_role = guild.get_role(lfg_role_id)

def initGameRoles(guild):
    global rankUpRole
    rankUpRole = guild.get_role(726184745863479386)
    global valorant_roles
    valorant_roles = {}
    valorant_playing_roles_ids = {
    716255359089639454:718396584244805652,
    716255407286386769:718396716960710706
    }
    for channel_id, role_id in valorant_playing_roles_ids.items():
        valorant_roles[guild_channels[channel_id]] = guild.get_role(role_id)

######################################################

######################################################
#Looking for group block
#INIT the list that holds the lfg players (if the bot disconnects randomly)
def init_lfg():
    for member in lfg_role.members:
        lfg_lst.append(member)

#INIT the game channels based on the games list
def getGameChannel(game, guild):
    game = game.lower()
    res_channels = []
    for channel in guild.channels:
        if (channel.name.lower()).find(game) != -1 and not isinstance(channel, discord.CategoryChannel):
            res_channels.append(channel)
    return res_channels

#Helper to see if the player is in a certain group
def checkIfPlayerInGroup(group, playerToCheck):
    for player in group:
        if player == playerToCheck:
            return True
    return False

#Helper to see if the certain group is full
def checkIfGroupIsFull(group, cap):
    return len(group) == cap

async def wrongChannelError(channel):
    await channel.send("Wrong Channel. This command is used in the LFG chat channel!")
##################################################################

#Random message helper function
def selectRandomMsg():
    msgs = [
        'Hello, this is random',
        'Whisky19 is so awesome',
        'I\'m a BroBot'
    ]
    return random.choice(msgs)

##################################################################
#RPS Functions
#Function to choose one of the possible options
def getRPSChoice():
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

#Helper function to see who won the rps game
def checkRPSWinner(user_choice, bot_choice):
    if(user_choice == 'rock' and bot_choice == 'scissors'):
        return 'User'
    if(user_choice == 'paper' and bot_choice == 'rock'):
        return 'User'
    if(user_choice == 'scissors' and bot_choice == 'paper'):
        return 'User'
    if(user_choice == bot_choice):
        return 'Draw'
    return 'Bot'

#Random insult when the bot wins
def randomInsult():
    msgs = [
        'Man, you are so bad!',
        'Who won? I won!',
        'Damn you suck, my nana can play better!'
    ]
    return random.choice(msgs)
#################################################################

#################################################################
#DB Functions
#DB FIELDS
#_id = Key(Users id in discord)
#Peanuts = Amount of peanuts the user has
#Main = Valorant agent that the user is maining
#Rank = will be decided when API is released

async def rankUp(id):
    user = server.get_member(id)
    if rankUpRole not in user.roles:
        await user.remove_roles(server.get_role(477585080819253248))
        await user.add_roles(rankUpRole)


async def addUserRolePoint(id):
    role_points = await serverdb.addUserRolePoint(id)
    if role_points >= 60:
        await rankUp(id)


################################################################
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#BOT COMMANDS BLOCK

#Ready event
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    #getRules(RULES)
    getCommands(COMMANDS)
    serverdb.initDatabase()
    guilds = bot.guilds
    for guild in guilds:
        if guild.name == GUILD:
            global server
            server = guild
            initChannels(guild)
            initGameVoiceChannelValorant()
            initGameRoles(guild)
            initLFGRole(guild)
    init_lfg()
    global report_channel
    report_channel = bot.get_channel(718765433100173404)
    global bot_test_channel
    bot_test_channel = bot.get_channel(716899271269679216)
    bot.loop.create_task(test_bg_task())
    #await initRulesChannel(717481643199168624)
    
#Random Command
@bot.command(name='random', help='Sends a random message')
async def random_message(ctx):
    print(f'Random')
    response = selectRandomMsg()
    print(f'{response}')
    await ctx.send(response)

#Move To General Command
@bot.command(name='moveGeneral', help = 'Moving users test')
async def move_user(ctx):
    user = ctx.author
    channel = ctx.guild.get_channel(477484690589351993)
    await user.move_to(channel)

#Reset Commands Message Command - Only Me
@bot.command(name = 'ResetCommands')
@commands.is_owner()
async def ResetCommands(ctx):
    channel = bot.get_channel(718045620551548962)
    await channel.purge(limit = 100, check= check_channel_rules)
    await channel.send(commands)

#Reaction Event
@bot.event
async def on_raw_reaction_add(payload):
    print(f'Reaction')
    user = server.get_member(payload.user_id)
    if payload.channel_id == 717481643199168624 and user.name != 716871391173148672:
        print(f'Not bot reacted, user is {user.name}')
        print(f'{payload.emoji}')
        if str(payload.emoji) == '👍':
            print(f'Corrected Emoji')
            role = bot.get_guild(477484690589351981).get_role(477585080819253248)
            if role not in user.roles:
                print(f'Added role to {user.name}')
                await user.add_roles(role)

#RPS Command
@bot.command(name = 'rps', help='A fun rock paper scissors game')
async def playrps(ctx, choice):
    choice = choice.lower()
    print(f'{ctx.author.id}')
    if(choice == 'rock' or choice == 'paper' or choice == 'scissors'):
        player = ctx.author
        bot_choice = getRPSChoice()
        msg = "I play " + bot_choice.capitalize() + " against your " + choice.capitalize() + "\n"
        winner = checkRPSWinner(choice, bot_choice)
        if(winner == 'User'):
            await ctx.send(msg + player.name + " has won! You got 10 Peanuts!")
            serverdb.addScore(player.id, 10)
        elif(winner == 'Bot'):
            await ctx.send(msg + player.name + " has lost! BroBot got 10 Peanuts!\n" + randomInsult())
            serverdb.addScore('BroBot', 10)
        else:
            await ctx.send(msg + player.name + " has drawn with BroBot! You got 5 Peanuts!")
            serverdb.addScore(player.id, 5)
            serverdb.addScore('BroBot', 5)
    else:
        await ctx.send("What is " + choice + "? Please use Rock Paper Scissors")

#Peanut Count Command
@bot.command(name = 'PeanutCount', help='How many Peanuts you have!')
async def printPeanuts(ctx):
    score = serverdb.getScore(ctx.author.id)
    await ctx.send(ctx.author.name + " has " + str(score) + " Peanuts!")

#Peanut Count Leaders Command
@bot.command(name='Leaders', help='Leaderboard for Peanuts')
async def leaderPeanuts(ctx):
    ids = serverdb.getLeadersFromDB()
    msg = ""
    for i in range(0,min(5,len(ids)),1):
        if isinstance(ids[i][0],str):
            msg += ids[i][0] + ' ' + str(ids[i][1]) + ' Peanuts\n'
        else:
            msg += str(bot.get_user(ids[i][0]).name) + ' ' + str(ids[i][1]) + ' Peanuts\n'
    await ctx.send(msg)

#Coin Toss Command
@bot.command(name = 'CoinToss', help='Bet on a coin toss')
async def coinToss(ctx, choice='None', amount=10):
    choice = choice.lower()
    print(choice)
    if choice == 'None':
        await ctx.send('You must choose Head or Tails!')       
    elif choice == 'heads' or choice == 'tails':
        curr_user_score = serverdb.getScore(ctx.author.id)
        if amount > curr_user_score:
            await ctx.send('You only have ' + str(curr_user_score) + ', can\'t gamble more than you got')
        else:
            coin = random.choice(['heads', 'tails'])
            msg = 'The coin has decided!\nIt\'s ' + coin.capitalize() + '.\n'
            if coin == choice:
                msg += 'You won ' + str(amount) + ' Peanuts!\n'
                msg += 'You now have ' + str(curr_user_score + amount) + ' Peanuts.'
                serverdb.addScore(ctx.author.id, amount)
            else:
                msg += 'You lost ' + str(amount) + ' Peanuts!\n'
                msg += 'You now have ' + str(curr_user_score - amount) + ' Peanuts'
                serverdb.addScore(ctx.author.id, -amount)
            await ctx.send(msg)
    else:
        await ctx.send('What is ' + choice.capitalize() + '? Please use Heads or Tails')

#Looking for group Command
@bot.command(name = 'lfg', help = '')
async def lfg(ctx):
    if ctx.channel == ctx.guild.get_channel(718045521381556224):
        isPlaying = False
        for role in ctx.author.roles:
            if role in valorant_roles.values():
                isPlaying = True
        if lfg_role not in ctx.author.roles and not isPlaying:
            lfg_lst.append(ctx.author)
            await ctx.author.add_roles(lfg_role)
            msg = ''
            msg += ctx.author.name + ' was added to the ' +  ' LFG Group.\n'
            msg += 'There are ' + str(len(lfg_lst)) + ' Looking for a group, use !lfp to see them.\n'
            count_channels = 0
            for channel in game_voice_channels_valorant:
                if len(channel.members) != 0:
                    msg += 'There are ' + str(len(channel.members)) + ' player in ' + str(channel.name) + '\n'
                    count_channels += 1
            if count_channels == 0:
                msg += 'There are no groups currently playing.'
            await ctx.send(msg)
            for role in valorant_roles.values():
                if len(role.members) != 0:
                    await ctx.send(role.mention + ' ' + str(ctx.author.name) + ' looking for a group')
        elif isPlaying:
            await ctx.send('You are already playing!')
        else:
            await ctx.send('You are already in LFG group!')
    else:
        await wrongChannelError(ctx.channel)

 #Looking for players command   
@bot.command(name = 'lfp')
async def lfp(ctx):
    if ctx.channel == ctx.guild.get_channel(718045521381556224):
        msg = ''
        if len(lfg_lst) != 0:
            msg += 'Here are the player who are looking for a group:\n'
            for user in lfg_lst:
                msg += str(user.name) + '\n'
            await ctx.send(msg)
            for role in valorant_roles.values():
                if role in ctx.author.roles:
                    await ctx.send(lfg_role.mention + ' ' + role.name + ' looking for a player!')
        else:
            msg += 'There are no players looking for a group.'
            await ctx.send(msg)
    else:
        await wrongChannelError(ctx.channel)

#Event related to the LFG Command
@bot.event
async def on_voice_state_update(member, before, after):
    await guild_channels[731572580519116852].send(str(member) + ", before " + str(before.channel) + ", after " + str(after.channel))
    if before.channel in valorant_roles.keys():
        await member.remove_roles(valorant_roles[before.channel])
    if after.channel in valorant_roles.keys():
        if member in lfg_lst:
            lfg_lst.remove(member)
            await member.remove_roles(lfg_role)
        await member.add_roles(valorant_roles[after.channel])

#Remove LFG Command    
@bot.command(name = 'removelfg')
async def removelfg(ctx):
    if ctx.channel == ctx.guild.get_channel(718045521381556224):
        member = ctx.author
        if member in lfg_lst:
            lfg_lst.remove(member)
            await ctx.author.remove_roles(lfg_role)
            await ctx.send('You were removed from the LFG List.')
        else:
            await ctx.send('You are not currently in the LFG List.')
    else:
        await wrongChannelError(ctx.channel)

#Who is playing Command
@bot.command(name = 'WhosPlaying')
async def WhosPlaying(ctx):
    if ctx.channel == ctx.guild.get_channel(718045521381556224):
        msg = 'Users that are playing right now:\n'
        for member in ctx.guild.members:
            for role in valorant_roles.values():
                if role in member.roles:
                    msg += str(member.name) + ' ' +str(role) +'\n'
        await ctx.send(msg)
    else:
        wrongChannelError(ctx.channel)

#Set Main Command
@bot.command(name = "SetMain")
async def setMain(ctx, mainAgent):
    mainAgent = mainAgent.lower()
    if mainAgent in agents:
        serverdb.setMainDB(ctx.author.id, mainAgent)
        await ctx.send(str(ctx.author.name) + ' is now maining ' + mainAgent.capitalize())
    else:
        await ctx.send("Is " + mainAgent.capitalize() + " a new Agent? I don't know him.")

#Getting your main Command
@bot.command(name = "Main")
async def getMain(ctx):
    mainAgent = serverdb.getMainAgentFromDB(ctx.author.id)
    if mainAgent == 'None':
        await ctx.send("You don't have a main!")
    else:
        await ctx.send(str(ctx.author.name) + ", your main is " + mainAgent + ".")

#Who is maining the agent Command
@bot.command(name = 'WhosMain')
async def whosMain(ctx, mainAgent):
    userList = serverdb.getMainListDB(mainAgent.lower())
    msg = ''
    msg += 'Users who are maining ' + mainAgent.capitalize() + '\n'
    for user in userList:
        msg += str(bot.get_user(user).name) + '\n'
    await ctx.send(msg)

#Report Command
@bot.command(name = 'Report')
async def report(ctx, *args):
    if(ctx.channel.id == 718765336002035722):
        msg = ''
        msg += str(ctx.author.name) + str(args)
        await ctx.send("Reported!")
        await report_channel.send(msg)
    else:
        await ctx.send("Please use the report channel")

#Clear LFG List - Only Me
@bot.command(name = 'Clearlfg')
@commands.is_owner()
async def clearlfg(ctx):
    for user in lfg_lst:
        await user.remove_roles(lfg_role)
    lfg_lst.clear()
    await ctx.send("Cleared LFG!")
    
#Set the rank command
@bot.command(name = "SetRank")
async def setRank(ctx, rank):
    rank = rank.lower()
    serverdb.setRankDB(ctx.author.id, rank)
    await ctx.send(str(ctx.author.name) + " is now ranked " + rank.capitalize())

#Get the rank Command
@bot.command(name = "Rank")
async def showRank(ctx,rank):
    rank = serverdb.getRankFromDB(ctx.author.id)
    if rank == 'None':
        await ctx.send("You do not have a rank")
    else:
        await ctx.send("Your rank is " + rank.capitalize())

#Showing all players with the Rank Command
@bot.command(name = 'ShowRank')
async def showAllRank(ctx, rank):
    rank = rank.lower()
    userList = serverdb.getRanksFromDB(rank)
    if len(userList) == 0:
        await ctx.send("There are no users with that rank!")
    msg = 'All players with rank ' + rank.capitalize() + '\n'
    for user in userList:
        msg += bot.get_user(user).name + '\n'
    await ctx.send(msg)

#Connect4 with ai command
@bot.command(name="connect4ai")
async def startConnect4AI(ctx):
    if ctx.channel.id == 731796875002249316 or ctx.channel.id == 716899271269679216:
        game_name = ctx.author.name+"aiconnect4"
        if gm.getGameFile(game_name):
            await ctx.send("You are already in a game!")
        else:
            gm.initGame(game_name)
            gm.moveConnect4(game_name, cAI.playMove(gm.getBoard(game_name)), 1)
            await ctx.send(file=discord.File(game_name+".png"))
            await ctx.send("Use !moveconnect4ai x (1<=x<=7) to add a move")
    else:
        await ctx.send("Wrong channel, use the minigames channel pls.")

#The command to start a move
@bot.command(name="moveconnect4ai")
async def moveConnect4AI(ctx, col : int):
    if ctx.channel.id == 731796875002249316 or ctx.channel.id == 716899271269679216:
        game_name = ctx.author.name+"aiconnect4"
        col -= 1
        if gm.getGameFile(game_name):
            if gm.moveConnect4(game_name, col, 2):
                if gm.gameWonConnect4(game_name, 2):
                    await ctx.send("You won! GG")
                    await ctx.send(file=discord.File(game_name + ".png"))
                    gm.removeGame(game_name)
                else:
                    while(not gm.moveConnect4(game_name, cAI.playMove(gm.getBoard(game_name)), 1)):
                        pass
                    await ctx.send(file=discord.File(game_name+".png"))
                    if gm.gameWonConnect4(game_name, 1):
                        await ctx.send("BroBot Won!")
                        gm.removeGame(game_name)
            else:
                await ctx.send("Illegal move!")
        else:
            await ctx.send("You are not in a game!")
    else:
        await ctx.send("Wrong channel, use the minigames channel pls.")


bot.run(TOKEN)
