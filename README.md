# BroBotValoran
Valorant BroBot

#Bot Commands
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

#Connect4ai
The ai uses Pillow to create the image for the game. It extracts data from the image every time a move is made and saves the game in a .png format.
The ai is made using minimax with alpha beta pruning with the depth of 7. It can still be optimized using bitmaps instead of the 2d array which may make it run faster in the calculations.

#Database
It uses the Mongo database server, basic stuff, nothing too big.
