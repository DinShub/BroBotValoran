# BroBotValorant

This project is for the bot in my discord channel.
The idea for the bot is to show and set stats, ranks and help with matching for queue and custom matches.

# Stats
In my discord channel we have a point system and I would like to use the api, so when a user (who opted to use this system) will earn points for a win, MVP and so on.
UPDATE: Based on the released API, this is the only possible thing right now.
I plan to make BroBot be able to extract the match history and statistics for a player, that authorized the Bot to do so, in order to show stats, win rate, and such. When more players on the server will allow the Bot to use their data, it will create stats based on teams that play in the server, who is the best team in the server. MVP players, and maybe more stuff I will think about it when programming it.
All the development for the bot will be documented here for Riot to observe to show I am not breaking any policies. The code itself for the bot will be private, since I am ashamed at my programming skills still (Only first year in Uni and a novice in Python)

# Ranks
I would like to utilize the ranking system in order to create an accesible way to match with players with similar ranks in my discord using the ranks in Valorant. The bot will get the rank of the user (when he decides to set his rank in discord), add it to the database I have for my server, and will show the rank of the selected user or the players with the requested rank. It will update the rank either manually or after a ranked match that the user has played (if he opted for automatic ranking).

# Queuing
I have a system in my discord to help the queuing process by showing the players who are playing or the players who are looking for a group to queue with. Using the discord command you will (if the api allows it) join you to the same party as the queuing group. Also using the rank system you can get automatched with people with the same rank who opted to use the auto matching system. Again, if the API allows it.

# Auto Custom Matching
If 10 people wants to play against each other, they can use the discord command to establish teams, veto maps and picking players (school football game style :D). After the team selection, veto and moving the users to the selected channels, it will group the players in game, select the correct map and the sides. Again, if the API will allow this system.

Those are my ideas right now, might expand or remove ideas based on the API and the suggestions from my discord users.
