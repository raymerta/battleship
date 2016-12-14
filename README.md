# Battleship
distributed system 2nd homework : battleship game


# Is Web Service a higher level representation of RPC?

Yes, it is. A web service is a specific implementation of RPC. At its lowest level, all a web service is, is connecting to a socket, using the HTTP protocol to negotiate sending a payload that is executed in a remote space (it may even be on the same computer, for all the consumer knows). All those abstractions are at its core RPC.

http://stackoverflow.com/questions/3028899/what-is-the-difference-between-remote-procedure-call-and-web-service


# How to run the game? 

## Installing RabbitMQ + WebStomp + Pika

- install rabbitMQ (https://www.rabbitmq.com/download.html)
- install web stomp (https://www.rabbitmq.com/web-stomp.html)
- install Pika (http://pika.readthedocs.io/en/0.10.0/) 

## running the game itself // need to be updated

- open terminal
- run rabbitMQ server and turn on web stomp plugin 
- run 'python server.py' 
- run 'python game.py'
- open Chrome browser, type 'http://localhost:10001/'

Notes: 

- ensure internet is connected to load assets (images, fonts, style, etc)
- prefer use Chrome browser for all players 
- clear all json files for better result except servers.json

# Development Strategy

We are copying server part from the first homework + rabbitMQ

# Testing

## Selecting server [Done]

- open Chrome browser, type 'http://localhost:10001/'
- pick one of the servers

expected result: user redirected to insert name page

## Dynamically update server [Need to refresh the page to update the list]

- open Chrome browser, type 'http://localhost:10001/'
- remove row from the list or add new list

expected result: without refreshing browser, server updated

## Insert username to server [Done]

- in insert username page, insert new username that never exist before
- press submit button

expected result: can create username, redirected to game session page

## Insert same username to same server [Done]

- in insert username page, insert new username that exist before
- press submit button

expected result: can't create username, stay in the page with error message,
showing the error message 'Given username is already taken. Please choose another.'

## Insert same username to different server [Doesn't pass, it shows Given username is already taken. Please choose another.]

- in insert username page, insert new username that never exist before
- press submit button

expected result: can create username, redirected to game session page

## create new game [Done] 

- open Chrome browser, type 'http://localhost:10001/'
- pick one of the servers
- insert unique username
- select 'New Game'
- Specefiy Number of players/ Game Tile Size and click Sumbit
- Select [Buttleship/Cruiser/Destroyer/Submarine] + the position
- Click Start Game

Expected result: Game started and the position saved.

## select existing game [Done]

- open Chrome browser, type 'http://localhost:10001/'
- pick one of the servers
- insert unique username
- select a server 
- Click Join
- Select [Buttleship/Cruiser/Destroyer/Submarine] + the position
- wait for the master player to start the battle

Expected result: New player joined the game if there is free space, and can select the buttleship and the position. 

## select existing game, game is running , and choose cancel

- open Chrome browser, type 'http://localhost:10001/'
- pick one of the servers
- insert unique username
- select a server 
- Click Join and start playing
- Click Cancel

Expected result:all ships have to be removed from the game field,
In case only one player is involved in the game and the others already left, the
game session should end


## select existing game, game is not running yet, and join



## select existing game, game is not running yet, and join but somebody already join

## The creator player notified for new player joined with his game session.

- open Chrome browser, type 'http://localhost:10001/'
- pick one of the servers
- insert unique username
- select 'New Game'
- Specefiy Number of players/ Game Tile Size and click Sumbit
- Player 2 Join the game session

Expected result: Server creater received a notification informing new player joined the game session

## start shooting each other

- Game session started
- Player 1 shoot - 1st attendence
- Player 2 shoot - 2nd attendence

Expected results: - Player 2 can't shoot before Player 1
                  - The serve notify the next one of his turn to shoot

## Special Case

- ensure testing crossbrowser connectivity


# TO DO: 

## important

### general

- handle URL hijacking

### server page

- dynamic server name from server [done]

### user page

- send user name to server [done]
- reject same name in same server [done]

### session page

- specify map size in new game [done]
- load existing open map [done]
- load existing game position

### game page

- toggle editing mode [done]
- get list of player [done]
- notification for game starting
- notification for player joining
- notification for player turn

## nice to have 

- [session] dynamic game session name [done]
- [username] check error when put duplicate name, it requires multiple clicking
- [creategame] limit number of player and tile size
- [game] change already positioned ship in the game
- [game] detect ship collision placement
- [game] change button color if all ship already placed

# Requirements
- User starts the application, and can select what game server to join [done]
  – The list of game servers is collected automatically by a client application (listening to server announces) done]
- User has to provide his nickname in order to join with the game [done]
  – After nickname is specified user may select the game server to play on [done]
- Server should not allow two users using the same nickname [done]
  – The player should be reject from joining the game server with the message to change his nickname. [done]
- Once user has joined the game server, it can either create a new game session or join existing one. [done]
- In case the user wants to create a new game session, he/she has need to provide the desired size of the battle field, then the new game field is created and the user has to position his ships on flat map (no obstacles, just water). Once the ships are positioned, the creator player should wait for someone to join his game session. The creator player must be notified each time new player joined with his game session. Once the creator player is satisfied with the number of players who have joined, he may trigger the start of a battle.[done]
- In case users want to join the existing game session, he/she has to position his ships and wait for the master player to start the battle. [done]
- Once the game session has a battle running the game server must preserve the order of players, allowing them to shoot one after the other. Each time the shoot is committed by a player, the server must notify the next one of his turn to shoot 
- Once the game session has a battle running the game server has to check the end-game condition, which is the situation where all the ships standing on the battlefield belong to only one player.
- Once the shoot is done by player the server must check the hit-conditions
  – if any ships were hit it should be visible for the player who triggered the shoot
  – the suffering player should see his ship attacked, and he/she should see the origin (who did attack him)
  – the other player should not see this positive hit
- Once the shoot is done by player the server must check the sink-conditions, in other words: if any ships were hit and if that hit made a ship sink (completely destroyed)
  – if any ships were sinked it should be visible for everyone at moment of sinking
- Once the player is out of the game he can do one of the following:
  – leave the game session
  – wait till the remaining players finish the session
    - while waiting the player sees everything all ships of all players as well as the scores and the damaged ships (so called spectator mode)
- Once the game session is finished the creator-player may restart the session.
- Player should be able to leave the game session at any moment (all his/her ships haveto be removed from the game field)
  – in case the creator-player is leaving the game-session the server selects the new owner among the remaining players
  – in case only one player is involved in the game and the others already left, the game session should end
- Player should be able to disconnect and connect again without loosing his game session
  – disconnecting should result in leaving the game session
  – in case the player did disconnect without leaving and he/she is not connected back for long time, then the creator player has liberty to withdraw the concerned player 
  – in case the creator player did disconnect without leaving and he/she is not connecting back long enough, the server selects the new owner among the remaining players
    - the previous creator-player can still connect back with lost ownership of the game session
  – in case game session was finished at the time the user is reconnecting, he/she should be informed and suggested to create or join another session

