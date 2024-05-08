from collections import Counter
class player:
    def __init__(self,name, conn, money = 5000):
        self.name = name
        self.highest = ()
        self.hand = []
        self.money = money
        self.initial_bet = 0
        self.host = False
        self.conn = conn
        self.room = None
    def __str__(self):
        return f"{self.name}"
    def print_value_of_hand(self,cards):
        values = [card.value for card in self.hand]
        print(values)

    def print_name_of_hand(self):
        return (f"Your hand: {[card.name for card in self.hand]}\n")

    def sort_hand_by_value(self,cards):
        return sorted(cards, key=lambda card: card.value,reverse=True)

    def highcard(self, highest, flop,ncard = None):
        all_cards = self.hand + flop
        high_cards =  [card for card in all_cards if card not in highest]
        high = self.sort_hand_by_value(high_cards)
        if ncard is not None:
            return high[:ncard+1]
        else:
            return high


    def hasStraightFlush(self, hand, flop):
        # Check if the player has a flush
        flush_value = self.hasFlush(hand, flop)
        if flush_value:
            # Check if the player has a straight within the flush cards
            flush_cards = self.filter_by_suit(hand + flop, flush_value[0].suit)
            straight_value = self.hasStraight(flush_cards, [])
            if straight_value:
                return straight_value  # Return the value of the highest card in the straight flush
        return None


    def hasPair(self,hand, flop):
        # Create a copy of the hand to avoid modifying the original list
        hand_copy = hand[:]
        # Extend the copy with the flop cards
        hand_copy.extend(flop)
        values = [card.value for card in hand_copy]
        value_counts = Counter(values)
        pairs = [value for value, count in value_counts.items() if count >= 2]
        if pairs:
            return pairs
        else:
            return None

    def has2pairs(self, hand, flop):
        # Create a copy of the hand to avoid modifying the original list
        hand_copy = hand[:]
        # Extend the copy with the flop cards
        hand_copy.extend(flop)

        values = [card.value for card in hand_copy]
        value_counts = Counter(values)

        pairs = [value for value, count in value_counts.items() if count >= 2]

        if len(pairs) >= 2:
            return sorted(pairs, reverse=True)[:2] # Return the two pairs
        else:
            return None


    def hasThree(self,hand, flop):
        # Create a copy of the hand to avoid modifying the original list
        hand_copy = hand[:]
        # Extend the copy with the flop cards
        hand_copy.extend(flop)
        values = [card.value for card in hand_copy]
        value_counts = Counter(values)
        three_of_a_kind = [value for value, count in value_counts.items() if count >= 3]
        if three_of_a_kind:
            return three_of_a_kind
        else:
            return None

    def hasSquad(self, hand, flop):
        # Create a copy of the hand to avoid modifying the original list
        hand_copy = hand[:]
        # Extend the copy with the flop cards
        hand_copy.extend(flop)
        values = [card.value for card in hand_copy]
        value_counts = Counter(values)
        squad = [value for value, count in value_counts.items() if count >= 4]
        if squad:
            return squad
        else:
            return None

    def hasFullHouse(self, hand, flop):
        # Create a copy of the hand to avoid modifying the original list
        hand_copy = hand[:]
        # Extend the copy with the flop cards
        hand_copy.extend(flop)
        # Count occurrences of each card value
        value_counts = Counter(card.value for card in hand_copy)
        # Check if there are exactly two distinct values: one with count 3 and another with count 2
        if {3, 2}.issubset(set(value_counts.values())):
            # Extract the values of three of a kind and pair
            three_of_a_kind = None
            pair = None
            for value, count in value_counts.items():
                if count == 3:
                    three_of_a_kind = value
                elif count == 2:
                    pair = value
            return [three_of_a_kind, pair]
        else:
            return None

    def hasStraight(self,hand, flop):
        # Create a copy of the hand to avoid modifying the original list
        hand_copy = hand[:]
        # Extend the copy with the flop cards
        hand_copy.extend(flop)

        # Extract values of the cards and sort them
        hand_copy = self.sort_hand_by_value(hand_copy)
        straight_list = []
        for i in range(len(hand_copy) - 1):
            current_value = hand_copy[i].value
            next_value = hand_copy[i + 1].value

            if next_value == current_value - 1:  # Cards are consecutive
                if hand_copy[i] not in straight_list and hand_copy[i+1] not in straight_list:
                    straight_list.append(hand_copy[i])
                    straight_list.append(hand_copy[i+1])
            elif next_value == current_value:  # Allow duplicates within a straight
                continue

            else:  # Cards are not consecutive, reset straight tracking
                straight_list = []

            if len(straight_list) >= 5:
                return straight_list[:5]
        return None  # No straight found
    def hasFlush(self,hand, flop,nmax = 0):
        # Create a copy of the hand to avoid modifying the original list
        hand_copy = hand[:]
        # Extend the copy with the flop cards
        hand_copy.extend(flop)
        # Count the occurrences of each suit
        suit_counts = {}
        for card in hand_copy:
            suit = card.suit
            suit_counts[suit] = suit_counts.get(suit, 0) + 1
        # Check if any suit occurs five or more times
        for suit, count in suit_counts.items():
            if count >= 5:
                flush_cards = self.filter_by_suit(hand_copy, suit)
                if nmax == 0:
                    return  self.sort_hand_by_value(flush_cards)
                else:
                    flush_cards = self.sort_hand_by_value(flush_cards)
                    return flush_cards[-nmax].value
        return None

    def fold(self):
        self.money -= self.initial_bet

    def call(self, current_bet):
        if self.money >= current_bet - self.initial_bet:
            print(f"{self.name} calls the bet of {current_bet}.")
            print("-"*20)
            self.money -= current_bet - self.initial_bet
            self.initial_bet = current_bet
            return True
        else:
            print(f"{self.name} doesn't have enough chips to call. They go all-in with {self.money} chips.")
            self.money = 0
            return False

    def bet(self, amount):
        if self.money >= self.initial_bet+amount:
            print(f"{self.name} bets {amount} money.")
            print("-" * 20)
            self.money -= amount
            self.initial_bet = self.initial_bet+amount
            return self.initial_bet
        else:
            print(f"{self.name} doesn't have enough money to bet. They go all-in with {self.money} chips.")
            bet_all_in = self.money
            self.money = 0
            return self.initial_bet+bet_all_in

    def raise_pot(self,amount):
        pass

    def filter_by_suit(self,cards, target_suit):
            return [card for card in cards if card.suit == target_suit]

    def determine_highest(self, flop):
        hand = self.hand
        # Check for various hand combinations starting from the strongest
        straight_flush = self.hasStraightFlush(hand, flop)
        if straight_flush:
            if straight_flush == 14:
                self.highest = (10, straight_flush)
            else:
                self.highest = (9, straight_flush)
            return

        squad = self.hasSquad(hand, flop)
        if squad:
            self.highest = (8, squad)
            return

        full_house = self.hasFullHouse(hand, flop)
        if full_house:
            self.highest = (7, full_house)
            return

        flush = self.hasFlush(hand, flop)
        if flush:
            self.highest = (6, flush)
            return

        straight = self.hasStraight(hand, flop)
        if straight:
            self.highest = (5, straight)
            return

        three_of_a_kind = self.hasThree(hand, flop)
        if three_of_a_kind:
            self.highest = (4, three_of_a_kind)
            return

        two_pairs = self.has2pairs(hand,flop)
        if two_pairs:
            self.highest = [3, two_pairs]
            return

        pair = self.hasPair(hand, flop)
        if pair:
            self.highest = (2, pair)
            return

        # If no strong hand is found, determine high card
        high_card = self.highcard([], hand)
        self.highest = (1, high_card)


