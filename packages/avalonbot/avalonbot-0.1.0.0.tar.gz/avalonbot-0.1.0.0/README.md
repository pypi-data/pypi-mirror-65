# avalon-bot
This is a bot to assist in playing [Avalon](https://hobbylark.com/card-games/How-to-Play-Avalon) online (e.g. over zoom). Given a configuration specifying the players, their emails, and the cards in the game, this bot will email each player their (randomly chosen) card, as well as additional privileged information appropriate to the player (e.g. it will tell the PERCIVAL player which two other players are either MORGANA or MERLIN, etc).

## Usage
```
git clone https://github.com/AvantiShri/avalon-bot
cd avalon-bot
./run_avalon_bot.py --game_name NameOfTheGame --smtp_server <smtp server> --json_config_file /path/to/game/config/file.json
```

## Result
Each player will get an email that looks something like this:
![](https://github.com/AvantiShri/avalon-bot/raw/master/ExampleEmail.png "Example Email")

## Config file format
See example_config/avalon_config.json for an example config file. The format of the config file is:
```
{
  "players: [
    {"name": "Name_of_player_1",
		 "email": "email.of@player1"},
		{"name": "Name_of_player_2",
		 "email": "email.of@player2"},
    (...additional player info, separated by commas...)
  ],
  "cards": [
      (This is a comma-separated list of the cards present in the game. If you have two of a particular type of card, repeat that card twice. The length of this list should be equal to the length of the "players" list. The possible cards are:)
      "LOYAL_SERVANT_OF_ARTHUR",
		  "MERLIN",
		  "PERCIVAL",
		  "MINION_OF_MORDRED",
		  "ASSASSIN",
		  "MORGANA",
		  "MORDRED",
		  "OBERON"
  ]
}
```

## Tips for playing on Zoom:

### Non-anonymous voting on who goes on a quest
Zoom's vote functionality is very finicky, so what my friends and I have done is have everyone enter their votes on the group chat simultaenously (someone will need to count down from three).

### Anonymous voting on whether a quest succeeds
Again, Zoom's vote functionality was very janky. What my friends and did instead was create a codeshare page (https://codeshare.io/new), and have everyone be present with their cursors poised (if players who are not on the quest have their cursors poised, that's fine too because it will help disguise who is who; it's also good to switch up the position of your cursor every now and then so that no one can keep track of which cursor belongs to whom). Have someone who is not on the quest count down from three, and then have the people on the quest enter their votes (yes or no) simultaneously.

### Keeping track of the vote count and whether quests have suceeded or failed
My friends and I tracked this by sending messages to the group chat, and it worked fine.

### Player order
Because the position of windows in zoom's gallery view can move around, we find it's best to just determine the player order alphabetically. Occasionally try reverse alphabetical order to switch things up.

### Other
- Decide in advance on whether or not you are going to allow sending PMs. The original game was designed to have everyone physically in the same room, so private communication wouldn't have been possible.
- The rules of Avalon are available online, e.g. [here](https://hobbylark.com/card-games/How-to-Play-Avalon) 
