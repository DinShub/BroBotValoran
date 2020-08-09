# BroBot

# Valorant
Valorant is the latest game from Riot. It is a 5 vs 5 Tactical shooters with Agents and economy styled gameplay. Users play as an agent that has special abilities
and must choose a right composition to win against the enemy team. Teamplay is the most important part of this game, that is why I made a bot to assist players
with finding teammates to play with, thus making callouts, team composition and similar ranks easier to handle rather than playing with random people.

# The Bot
This bot is for my personal server for the game Valorant.
The bot is made for easier LFG (Looking for a group) access and for some small minigames.
The main idea is that a user can use the command !lfg in the channel named LFG to annouce that he is looking for a group, in a addition he will get a special
role called LFG to be shown in a different users list that he is looking people to play with. When the user uses !lfg, players who are already playing (checked if they
are in the Valorant voice channels) will be tagged that a user is looking for a group.
In a addition to the lfg command, users who are playing and are in the Valorant voice channel get assigned a special role called Playing Valorant with the channel number 
and are in a list to show other users that there are people who are playing for easier access to find groups.
Another command is !lfp (looking for players) that users can use to get a list of the people who are in the LFG list, and the people in that list will also be pinged 
that a group is looking for players, thus notifing them that they can join a group to play with.
There is also a point system which works with a database to save the points and users can also set a main (!SetMain) agent so other users can find players (!WhosMain)
to complete their group composition.

# Bot Commands
Here are the bot commands for BroBot:
1. !random = BroBot will print a random message (does not have really a lot of messages)
2. !games = BroBot will print the games the !lfg commands work for
3. !rps choice = BroBot will play Rock Paper Scissors with you (raplace choice with Rock, Paper or Scissors)
4. !PeanutCount = BroBot will show you how many Peanuts you have (Earn Peanuts by winning in !rps or !CoinToss)
5. !leaders = BroBot will show you who are the leader by Peanut PeanutCount
6. !CointToss choice amount = BroBot will toss a coin (replace choice with Heads or Tails) (replace amount with the amount to gamble, default is 10)
7. !lfg= BroBot will add you to the LFG group and will tell you if a group is currently playing
8. !lfp = BroBot will show you the players currently looking for a group
9. !removelfg= BroBot will remove you from the LFG group if you are listed there
10. !WhosPlaying = BroBot will show you whos is currently playing
11. !SetMain main = BroBot will set you Valorant Main Agent (replace main with your agent)
12. !Main = BroBot will show you who you set as your Main Valorant Agent
13. !WhosMain main = BroBot will show you all the players with that main (replace main with an agent)
14. !connect4ai = Start a connect4 match against the ai
15. !moveconnect4ai x = enter a piece into the x column (1-6)

# Connect4ai
The ai uses Pillow to create the image for the game. It extracts data from the image every time a move is made and saves the game in a .png format.
The ai is made using minimax with alpha beta pruning with the depth of 7. It can still be optimized using bitmaps instead of the 2d array which may make it run faster in the calculations.

# Database
It uses the Mongo database server, basic stuff, nothing too big.
