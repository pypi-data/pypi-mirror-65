from __future__ import division, print_function, absolute_import
import random
from collections import OrderedDict
from .cards import Team
from collections import Counter


class Player(object):

    def __init__(self, email, name):
        self.email = email
        self.name = name

    def assign_card(self, card):
        self.card = card

    def __str__(self):
        return self.name


class Game(object):

    def __init__(self, players, cards):
        assert len(players)==len(cards),\
               ("Please specify as many cards as players!"
                +"\n#Players is "+str(len(players))
                +"\n#Cards is "+str(len(cards)))
        self.players = players
        self.cards = cards 

    def assign_cards_to_players(self):
        #randomly shuffle the order of the cards
        shuffled_cards = [x for x in self.cards]
        random.shuffle(shuffled_cards)
        for player, card in zip(self.players, shuffled_cards):
            player.assign_card(card)

    def prepare_secret_info_to_tell_each_player(self):
        secret_info = {}
        for player in self.players:
            secret_info[player] = OrderedDict([
            ('Your card is:', str(player.card.card_type)),
            ('Your team is:', str(player.card.team) ),
            ('Your special abilities (if any):',
             player.card.special_abilities),
            ('Additional info you have (if any)',
             player.card.get_additional_info_to_provide_to_player(game=self))])
        return secret_info

    def prepare_info_on_cards_types(self):
        card_info = OrderedDict()
        for card in self.cards:
            if card.card_type not in card_info:
                card_info[str(card.card_type)] = card.get_card_summary()
        return card_info

    def prepare_info_on_teams(self):
        good_team_cards = Counter([str(x.card_type) for x in self.cards if
                                   x.team==Team.GOOD])
        bad_team_cards = Counter([str(x.card_type) for x in self.cards if
                                   x.team==Team.EVIL])
        return good_team_cards, bad_team_cards
