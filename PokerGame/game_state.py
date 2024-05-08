import enum


class game_state:
    def __init__(self, deck, player_list, current_bet = 0, round = 0):
        self.flop = []
        self.current_bet = current_bet
        self.round = round
        self.pot = 0
        self.highest_better = None
        self.active_players = player_list.copy()
        self.deck = deck
        self.next = False
        self.first_index=0
        self.Current_first_index=self.first_index
        self.player_list = player_list
        self.current_player=player_list[self.first_index]
        self.checked = []
        self.called = []
        self.folded=[]
        self.winner=None