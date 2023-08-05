from __future__ import division, print_function, absolute_import
from .game import Game
from .cards import card_type_to_class
import json


def create_cards(card_strings):
    cards = []
    for card_type in card_strings:
        cards.append(card_type_to_class[card_type]())
    return cards


def send_email(subject, to_addresses,
               sender, #eg: "avutils-mail-sender@stanford.edu",
               password,
               smtp_server, #eg: "smtp.stanford.edu",
               contents=""):
    from email.mime.text import MIMEText
    import smtplib
    msg = MIMEText(contents)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ",".join(to_addresses)

    if (":" in smtp_server):
        smtp_server, port = smtp_server.split(":")
        s = smtplib.SMTP(smtp_server, port=int(port))
    else:
        s = smtplib.SMTP(smtp_server)
    s.starttls();
    if (password is not None):
        s.login(sender, password)
    s.sendmail(sender, to_addresses, msg.as_string())
    s.quit()


def json_dump(obj):
    return json.dumps(obj, indent=4, separators=(',', ': '))


def launch_game(players, cards, game_name, sender, password, smtp_server):
    game = Game(players=players, cards=cards) 
    game.assign_cards_to_players()

    secret_info = game.prepare_secret_info_to_tell_each_player() 
    card_types_info = game.prepare_info_on_cards_types()
    good_team_cards, bad_team_cards = game.prepare_info_on_teams()

    for player,private_info in secret_info.items():
        contents = ("Hi "+player.name+",\n"
                    "Here is your avalon card assignment:\n"
                    +json_dump(private_info)+"\n"
                    +"\nHere is info on the cards present in this game:\n"
                    +"\nCards for the good team:\n"
                    +json_dump(good_team_cards)+"\n"
                    +"\nCards for the bad team:\n"
                    +json_dump(bad_team_cards)+"\n"
                    +"\nDescriptions of each card:\n"
                    +json_dump(card_types_info))
        
        send_email(subject="Your Avalon Card Assignment for "
                           +"game: "+str(game_name),
                   to_addresses=[player.email],
                   sender=sender,
                   password=password,
                   contents=contents,
                   smtp_server=smtp_server) 
