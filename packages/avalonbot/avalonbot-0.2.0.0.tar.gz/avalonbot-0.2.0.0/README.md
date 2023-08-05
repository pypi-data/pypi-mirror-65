# avalon-bot
This is a bot to assist in playing [Avalon](https://hobbylark.com/card-games/How-to-Play-Avalon) online (e.g. over zoom). Given a configuration specifying the players, their emails, and the cards in the game, this bot will email each player their (randomly chosen) card, as well as additional privileged information appropriate to the player (e.g. it will tell the PERCIVAL player which two other players are either MORGANA or MERLIN, etc). In other words, each player will get an email that looks something like this:
![](https://github.com/AvantiShri/avalon-bot/raw/master/ExampleEmail1.png "Example Email")

## Running from Google Colab (recommended for people unfamiliar with the command line)

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

## Running from the Command Line (for people who prefer it)

This package is on pypi and can be installed with pip:
```
pip install avalonbot
```

The bot can then be run with:
```
run_avalon_bot --game_name YourGameNameHere --smtp_server specify.your.smtp.server --sender email.for.bot@example.com [--password passwordforbot] --json_config_file /path/to/json_config.json
```

### Config file format
See example_config/avalon_config.json for an example config file. The format is:
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
      (This is a comma-separated list of the cards
       present in the game. If you have two of a particular
       type of card, repeat that card twice. The length of this
       list should be equal to the length of the "players" list.
       The possible cards are:)
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
