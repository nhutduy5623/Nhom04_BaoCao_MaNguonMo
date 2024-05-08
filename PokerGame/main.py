import subprocess
import re

import requests

from deck import Deck
from player import player
import socket
import threading
from game_state import game_state
import pickle
poker_ranks = {
    "High Card": 1,
    "One Pair": 2,
    "Two Pair": 3,
    "Three of a Kind": 4,
    "Straight": 5,
    "Flush": 6,
    "Full House": 7,
    "Squad": 8,
    "Straight Flush": 9,
    "Royal Flush": 10
}

poker_rounds = {
    0: "Preflop",
    1: "Flop",
    2: "Turn",
    3: "River",
    4: "Showdown"
}
connected_clients = {}
state = None
def print_name_of_flop(flop):
    print("-" * 30)
    return (f"Flop: {[card.name for card in flop]}")


def print_current_round(round_number):
    if round_number in poker_rounds:
        return f"Current Round:  {poker_rounds[round_number]}"
    else:
        return ("Invalid round number.")


def print_action(player, current_bet):
    s = ""
    if current_bet == 0:
        s = "1.Bet  2.Fold  3.Check \n"
    else:
        s = "1.Call  2.Raise  3.Fold \n"
    s += player.print_name_of_hand() + (f"Your Money: {player.money}")
    return s


def game(player_list):
    deck = Deck()
    deck.shuffle()
    small_blind = 5
    global state
    player_in_room = list(player_list)
    state = game_state(deck, reset_players_hand(player_list), small_blind * 2)
    dealCards(player_list, state.deck)
    state.pot = make_pot(state.player_list,state.first_index, small_blind, state.pot)

    # # 5 rounds of poker loop
    # for i in range(5):
    #     print(i)
    #     state.round = i
    #     if len(state.player_list) == 1:
    #         print(f"{player_list[0].name} wins")
    #         state.player_list[0].money += state.pot
    #         broadcast_to_others(state.player_list[0], player_in_room, "wins")
    #         break
    #     state.current_bet = 0
    #     if i == 0:
    #         state.pot = make_pot(state.player_list, small_blind, state.pot)
    #         state.current_bet = small_blind * 2
    #     if i == 1:
    #         flop_deal(state.flop, state.deck)
    #     elif i == 2 or i == 3:
    #         state.flop.append(state.deck.draw_card())
    #     # last round
    #     elif i == 4:
    #         winner = showdown(state.player_list, state.flop)
    #         if type(winner) is list:
    #             for player in winner:
    #                 print(f"{player.name} wins")
    #                 broadcast_to_others(winner, player_in_room, "wins")
    #                 player.money += state.pot // len(winner)
    #         else:
    #             broadcast_to_others(winner, player_in_room, "wins")
    #             winner.money += state.pot
    #         break
    #     put_money_into_pot(state)
    #     state.player_list = reset_players_bet(state.player_list)
    #     # loop stop if its go back to highest_better
    #     state.highest_better = state.player_list[-1]
    #     state.checked = []
    #     if state.round == 0:
    #         state.active_player = state.player_list[0]
    #     # loop to end round if all players have checked or called the highest raise/bet
    #     while True:
    #         if len(state.player_list) == 1:
    #             break
    #         player = state.active_player
    #         if state.round == 0 and state.highest_better is player and state.current_bet != small_blind * 2:
    #             break
    #         # player is the highest_better and has made a bet, used for round > 0
    #         if state.round > 0 and player is state.highest_better and state.current_bet == player.initial_bet and state.current_bet != 0:
    #             break
    #         # players action
    #
    #         send_available_action(player, state.player_list, state)
    #         # loop to wait for player's action
    #         while state.active_player is player:
    #             pass
    #
    #         # if all check
    #         if state.round > 0 and len(state.checked) == len(state.player_list):
    #             break
    #
    #         # condition to break, used for preflop(round = 0) only
    #         # if this is a last player, and they don't make the bet(current_bet == small_blind)
    #         if state.round == 0 and state.highest_better is player and state.current_bet == small_blind * 2:
    #             break



def put_money_into_pot(state):
        for player in state.player_list:
            if player.initial_bet!=-1:
               state.pot += player.initial_bet
               player.initial_bet=0


def reset_players_bet(player_list):
    for player in player_list:
        player.initial_bet = 0
    return player_list


def reset_players_hand(player_list):
    for player in player_list:
        player.hand = []
        player.initial_bet=0
    return player_list


def send_available_action(player, player_list, state):
    s = f"{player.name} TURN\n"
    if state.round != 0:
        s += print_name_of_flop(state.flop) + "\n"
    s += print_current_round(state.round) + "\n"
    s += print_action(player, state.current_bet) + "\n"
    s += (f"Current bet: {state.current_bet}") + "\n"
    s += (f"Current pot: {state.pot}") + "\n"
    player.conn.sendall(s.encode())
    if player.host:
        choice = player.conn.recv(1024).decode().split()[2]
        process_action(player, player_list, choice)


def process_action(player, player_list, data):
    global state
    player_index = player_list.index(player)
    choice=data.split()[1]
    if choice == "1":
        if state.current_bet != 0:
            player.call(state.current_bet)

    elif choice == "2":
        state.pot+=player.initial_bet
        player.initial_bet=-1
        state.active_players.remove(player)
        # else:
        #     player.conn.sendall("Enter the amount".encode())
        #     bet_amount = int(player.conn.recv(1024).decode().split()[2])
        #     if int(bet_amount) < state.current_bet:
        #         player.conn.sendall("Amount not valid!").encode()
        #     else:
        #         player.bet(bet_amount)
        #         state.current_bet = bet_amount
        #         state.highest_better = player
        #         broadcast_to_others(player, player_list, f"Raise {bet_amount}")
    elif choice == "3":

        bet_amount=int(data.split()[2])
        amount=player.bet(bet_amount)
        if state.current_bet > 0:
            state.current_bet=amount
        else:
            state.current_bet = bet_amount
        state.highest_better = player

        #     player.fold()
        #     print(f"{player.name} fold")
        #     broadcast_to_others(player, player_list, "Fold")
        #     player_list.remove(player)
        # else:
        #     broadcast_to_others(player, player_list, "Check")
        #     print(f"{player.name} check")
        #     state.checked.append(player.name)
    if (len(state.active_players) == 1):
        put_money_into_pot(state)
        winner=state.active_players[0]
        winner.money += state.pot
        state.winner=winner
    player_temp=player_list[state.Current_first_index]
    while(player_temp.initial_bet==-1 or player_temp.money==0):
        state.Current_first_index+=1
        player_temp = player_list[state.Current_first_index]
    try:
        player_index = player_list.index(player)
        next_player_index = player_index + 1
        while(next_player_index<len(player_list)):
            player_temp = player_list[next_player_index]
            if not (player_temp.initial_bet == -1 or player_temp.money == 0):
                if not (player_temp.initial_bet==state.current_bet and state.current_bet>0):
                    break
            next_player_index += 1




    except ValueError:
        # not found because player had folded
        next_player_index = player_index
    if next_player_index >= len(player_list):
        if(state.current_player.initial_bet==player_list[state.Current_first_index].initial_bet):
            processing_game()
        state.current_player = player_list[state.Current_first_index]
    else:
        state.current_player = player_list[next_player_index]

def processing_game():
    global state

    if len(state.flop)==0:
        flop_deal(state.flop, state.deck)
        put_money_into_pot(state)
        state.current_bet = 0
    elif(len(state.flop)==5):
        put_money_into_pot(state)
        winner = showdown(state.active_players, state.flop)
        if type(winner) is list:
            for player in winner:
                player.money += state.pot // len(winner)
        else:
            winner.money += state.pot
        state.winner=winner

    else:
        state.flop.append(state.deck.draw_card())
        put_money_into_pot(state)
        state.current_bet=0

def make_pot(player_list,first_index, small_blind, pot):
    small = player_list[first_index]
    big = player_list[first_index+1]
    small.money -= small_blind
    big.money -= small_blind * 2
    small.initial_bet = small_blind
    big.initial_bet = small_blind * 2
    pot =0
    return pot


# args: a list of players and flop cards
# return: a list of winner
def showdown(players, flop):
    for player in players:
        player.determine_highest(flop)
    # Sort players by the rank of their highest hands
    players.sort(key=lambda x: (x.highest[0]), reverse=True)
    highest_hand = players[0].highest[0]
    # Check if there's a single winner
    highest_players = filter_by_highest_hand(players, highest_hand)
    if len(highest_players) == 1:
        return highest_players[0]
    # more than 2 players have the same rank
    else:
        # royal flush
        if highest_hand == 14:
            return highest_players
        # straight and straight flush
        elif highest_hand == 5 or highest_hand == 9:
            return find_player_with_n_highest_value(highest_players)
        # squad
        elif highest_hand == 8:
            highest_players = find_player_with_n_highest_value(highest_players)
            if len(highest_players) == 1:
                return highest_players
            # if there are players that have the same value and rank, then we compare their high card
            else:
                return compare_high_cards(highest_players, flop, 1)
        # full house
        elif highest_hand == 7:
            highest_players = find_player_with_n_highest_value(highest_players)
            if len(highest_players) == 1:
                return highest_players
            else:
                return find_player_with_n_highest_value(highest_players, 1)
        # flush
        elif highest_hand == 6:
            for i in range(5):
                highest_players = find_player_with_n_highest_value(highest_players, i)
                if len(highest_players) == 1:
                    return highest_players
            return highest_players
        # 2 pairs
        elif highest_hand == 3:
            highest_players = find_player_with_n_highest_value(highest_players)
            if len(highest_players) == 1:
                return highest_players
            else:
                highest_players = find_player_with_n_highest_value(highest_players, 1)
                # if there are players that have the same value and rank, then we compare their high card
                return compare_high_cards(highest_players, flop, 1)
        # three
        elif highest_hand == 4:
            highest_players = find_player_with_n_highest_value(highest_players)
            if len(highest_players) == 1:
                return highest_players
            # if there are players that have the same value and rank, then we compare their high card
            else:
                return compare_high_cards(highest_players, flop, 2)
        # pair
        elif highest_hand == 2:
            highest_players = find_player_with_n_highest_value(highest_players)
            if len(highest_players) == 1:
                return highest_players
            # if there are players that have the same value and rank, then we compare their high card
            else:
                return compare_high_cards(highest_players, flop, 3)
        # high card
        elif highest_hand == 1:
            return compare_high_cards(highest_players, flop, 7)


def compare_high_cards(highest_players, flop, number_of_high_cards):
    # calculate high card by removing best hand combination
    for player in highest_players:
        if player.highest[0] == 1:
            pass
        else:
            player.highest = [1, player.highcard(player.highest[1], flop, number_of_high_cards)]
    for i in range(number_of_high_cards):
        highest_players = find_player_with_n_highest_value(highest_players, i)
        if len(highest_players) == 1:
            return highest_players
    return highest_players


def find_player_with_n_highest_value(players, n=0):
    highest_value = 0
    for player in players:
        if type(player.highest[1][n]) is int:
            if player.highest[1][n] >= highest_value:
                highest_value = player.highest[1][n]
        else:
            if player.highest[1][n].value >= highest_value:
                highest_value = player.highest[1][n].value
    if type(players[0].highest[1][n]) is int:
        return [p for p in players if p.highest[1][n] >= highest_value]
    return [p for p in players if p.highest[1][n].value >= highest_value]


def filter_by_value(players, value):
    return [player for player in players if player.highest[1][0] == value]


def dealCards(p_list, deck):
    for player in p_list:
        for _ in range(2):
            player.hand.append(deck.draw_card())


def flop_deal(flop, deck):
    for _ in range(3):
        flop.append(deck.draw_card())


def filter_by_highest_hand(players, target):
    return [player for player in players if player.highest[0] == target]


HOST = 'localhost'  # Replace with actual server IP if needed
PORT = 65432


# Define dictionary to store connected clients and their room IDs
def getHands(hands):
    myCards=[f"{card}" for card in hands]
    return pickle.dumps(myCards)
def getPlayers(player,player_list):

    player_index = player_list.index(player)
    player_list.pop(player_index)
    myList=[]
    for player1 in player_list:
        myList.append((player1.name,player1.initial_bet,player1.money,player1.hand))
    return pickle.dumps(myList)
def getWinner(winner,pot):
    s="Winner "
    if type(winner) is list:
        for w in winner:
            s+=f" {w.name}"
    else:
        s+= winner.name
    s+= f" win the pot : {pot}"
    return s


def handle_client(conn, addr):
    global connected_clients
    """Handles communication with a connected client."""
    print(f'Connected by {addr}')
    current_player = None
    try:
        # Check for JOIN message format
        data = conn.recv(1024).decode()
        if data.startswith("JOIN"):
            try:
                room_id = int(data.split()[1])
                name = data.split()[3]
                # Create room if it doesn't exist
                if room_id not in connected_clients:
                    connected_clients[room_id] = []
                    # connected_clients[room_id].append()
                # Add client to the room
                current_player = player(name, conn)
                current_player.room = room_id
                if len(connected_clients[room_id]) == 0:
                    current_player.host = True
                    conn.sendall(f'{current_player.name} created room successfully! You are the host.'.encode())
                else:
                    conn.sendall('Joined room successfully!'.encode())
                connected_clients[room_id].append(current_player)
                print(f'Client {addr} joined room {room_id}')
            except (ValueError, IndexError):
                conn.sendall('Invalid room ID format. Please use JOIN <number>'.encode())
                return  # Exit the loop on invalid format
            # ... remaining logic for messages within the room ...
        else:
            conn.sendall('Invalid message format.'.encode())
            return  # Exit the loop on invalid format
        # Broadcast messages to clients in the same room
        while True:
            room_clients = connected_clients.get(room_id)

            data = conn.recv(1024).decode()
            if not data:
                break
            # Print the received message (optional)
            if data=="get_number":
                conn.sendall(f"{len(room_clients)}".encode())
            if data == "get_players":
                conn.send(getPlayers(current_player,state.player_list.copy()))
            if data == "get_hands":
                conn.send(getHands(current_player.hand))
            if data=="START":
                game(room_clients.copy())
                conn.send(f"nothing".encode())
            if data=="get_playerMoney":
                conn.send(f"{current_player.money}".encode())
            if data == "get_pot":
                conn.send(f"{state.pot}".encode())
            if data=="get_playerBet":
                conn.send(f"{current_player.initial_bet}".encode())
            if data=="get_winner":
                if(state.winner):
                    conn.send(getWinner(state.winner,state.pot).encode())
                else:
                    conn.send(f"notthing".encode())
            if data=="get_currentBet":
                conn.send(f"{state.current_bet}".encode())
            if data == "get_turn":
                conn.send(f"{state.current_player==current_player}".encode())
            if data == "can_start":
                if state!=None:
                    if state.winner==None:
                        conn.send(f"True".encode())
                    else:
                        conn.send(f"False".encode())
                else:
                    conn.send(f"False".encode())
            if data == "get_flop":
                conn.send(getHands(state.flop))
            elif len(room_clients) < 2:
                data = "Not enough player"
            elif data.startswith("ACTION"):
                # Process the action and update the game state

                process_action(current_player, state.player_list, data)

                conn.send(f"nothing".encode())

    except ConnectionError as e:
        print(f'Error communicating with client {addr}: {e}')
    finally:
        if current_player is not None:
            if current_player.host:
                host_index = connected_clients[room_id].index(current_player)
                if host_index + 1 < len(connected_clients[room_id]):
                    new_host = connected_clients[room_id][host_index + 1]

                else:
                    new_host = connected_clients[room_id][0]
                new_host.host = True
                new_host.conn.sendall(f'{new_host.name} created room successfully! You are the host.'.encode())
            connected_clients[room_id].remove(current_player)
            conn.close()
            print(f'Client {addr} disconnected.')


def broadcast_to_others(current_player, player_list, action):
    if type(current_player) is not list:
        for player in player_list:
            message = f"{current_player.name} {action}"
            player.conn.sendall(message.encode())
    else:
        player_names = ', '.join([player.name for player in current_player])
        message = f"{player_names} {action}"
        for player in player_list:
            player.conn.sendall(message.encode())



def get_ngrok_assigned_port():
    url = "http://127.0.0.1:4040/api/tunnels"
    try:
        response = requests.get(url)
        url_new_https = response.json()["tunnels"][0]["public_url"]
        return url_new_https
    except:
        return None
    # print(json.dumps(r.json(), indent=4))
    # pprint.pprint(r, width=1)

# Example usage:
def updateServerAddress(address):
    url = "https://poker-address-api.vercel.app/"

    # Define the data to be sent in the request body
    data = {"address": address}
    # Send the PUT request
    response = requests.put(url, json=data)

    # Check the response status code
    if response.status_code == 200:
        print(address)
        print("PUT request successful")

    else:
        print("PUT request failed with status code:", response.status_code)


assigned_port = get_ngrok_assigned_port()
if assigned_port:
    updateServerAddress(assigned_port)
else:
    print("Failed to obtain assigned port from Ngrok.")

def main():
    """Starts the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server listening on {HOST}:{PORT}')

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()


if __name__ == '__main__':
    main()
