import random
#import tflearn
import numpy as np
import sys
import os
import pickle
#from tflearn.layers.core import input_data, dropout, fully_connected
#from tflearn.layers.estimator import regression
import time
from matplotlib import pyplot as plt
from Basic_Strategy import Basic_Strategy

number_of_decks = 4
games_between_shuffle = 8
number_of_games = 500

your_score_tot = [0]
training_data = []
accepted_scores = []

# Disable printing
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
# Restore printing
def enablePrint():
    sys.stdout = sys.__stdout__

#blockPrint()

class card:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class player:
    global game_over
    global deck
    global no_of_remaining_cards

    def __init__(self, inplay, score=1, finished=False):
        self.inplay = inplay
        self.can_split = True
        self.score = score
        self.cards = []
        self.total = 0
        self.finished = finished
        self.blackjack_check = False

    def update_total(self):
        total = 0
        for card in self.cards:
            total += card.value
        self.total = total

    def draw_card(self):
        global no_of_remaining_cards

        card_index_to_draw = random.randrange(no_of_remaining_cards - 1)
        drawn_card = deck.pop(card_index_to_draw)
        self.cards.append(drawn_card)
        no_of_remaining_cards -= 1



        for card in self.cards:
            if card.name == 'A':
                card.value = 11

        # Sums the Total of the Players Cards.
        self.update_total()

        # converts an ace into 1 if total over 21
        for card in self.cards:
            if self.total > 21:
                if card.value == 11:
                    card.value = 1

        # Sums the Total of the Players Cards.
        self.update_total()

        return drawn_card

    def check_bust(self):
        if self.total > 21:
            return True
        else:
            return False

    def can_split_check(self):
        if str(self.cards[0].name) == str(self.cards[1].name):
            self.can_split = True
            print(self.cards[0].name, self.cards[1].name)
        else:
            self.can_split = False

    def check_soft(self):
        for card in self.cards:
            if card.value == 11:
                return True
        return False

    def split(self):
        return self.cards.pop(0)

    def double(self):
        self.score += 1
        self.draw_card()


# All the Cards
two = card('2',2)
three = card('3',3)
four = card('4',4)
five = card('5',5)
six = card('6',6)
seven = card('7',7)
eight = card('8',8)
nine = card('9',9)
ten = card('10',10)
jack = card('J',10)
queen = card('Q',10)
king = card('K',10)
ace = card('A',11)

suit = [two,three,four,five,six,seven,eight,nine,ten,jack,queen,king,ace]
new_deck = 4 * suit * number_of_decks

hand_no = 0
your_score = 0

line = "------------------------------------"


def show_hands(hands, hand_count=0):
    print('--==[Your Cards]==--')
    for hand_no, hand in enumerate(hands):
        if hand_no == hand_count:
            print('> ',end='')
        for card in hand.cards:
            print(f'[{card.name}]', end=" ")
        hand.update_total()
        print(f'Total: {hand.total}')

def is_bust(hand,hands):
    global your_score
    if hand.check_bust():
        hands.remove(hand)
        hand.inplay = False
        print('You have gone bust.')
        hand.score = -hand.score
        hand.finished = True
        return True
    else:
        return False

def split_hand(hand,num):
    global hands
    name = 'you' + str(num)
    name = player(True) # Create a new hand
    name.cards.append(hand.split()) # append the one of the cards from the orignal hand to it
    name.draw_card()
    hand.draw_card()
    hands.append(name)

def game(number_of_games=1):
    global no_of_remaining_cards
    global deck
    global your_score
    global hands

    split_count = 0

    game_memory = []

    x=0
    while x < number_of_games:
        print('Game Number: ',x)
        count = 0
        deck = new_deck.copy()
        you = player(True)
        you2 = player(False)
        you3 = player(False)
        you4 = player(False)

        dealer = player(True)

        hands = [(you)]

        count += 1
        if count == games_between_shuffle:
            deck = new_deck.copy()
            count = 0
            print('DECK SHUFFLED')
        no_of_remaining_cards = 52

        your_go_over = False
        dealers_go_over = False
        game_over = False
        hands_played = 0

        you.draw_card()
        dealer.draw_card()
        you.draw_card()
        dealer.draw_card()

        print(f'Dealer: [{dealer.cards[0].name}] [?]')
        show_hands(hands)

        # Players Turn
        hand_count = 0
        for hand in hands:
            while not hand.finished:
                # Checks for Black Jack
                if not hand.blackjack_check:
                    hand.blackjack_check = True
                    if hand.total == 21:
                        if dealer.cards[0].value != 10: # If the dealer has no ace or 10
                            if dealer.cards[0].value != 11:
                                print('YOU WIN - BLACK JACK')
                                your_score += 1.5
                                hand.finished = True
                                dealers_go_over = True

                if not hand.finished:
                    # Check if cards are matching
                    hand.can_split_check()
                    if len(hand.cards) != 2:
                        hand.can_split = False
                    if hand.can_split:
                        split_text = f" - Split (sp)"
                    else:
                        split_text = ""

                    player_input = input(f'Stick (s) - Hit (h) - Double (d){split_text}: ')
                    print('tot:',int(hand.total), '| dealer:',str(dealer.cards[0].value),'| soft:', hand.check_soft(),'| split:', hand.can_split)

                    ##############################################
                    '''observations = (hand.total, dealer.cards[0].value, hand.check_soft(), hand.can_split)
                    if hand.can_split:
                        player_input = random.choice(['s', 'h', 'd', 'sp'])
                    else:
                        player_input = random.choice(['s', 'h', 'd'])

                    game_memory.append((observations, player_input))'''


                    #player_input = Basic_Strategy(int(hand.total), str(dealer.cards[0].name), hand.check_soft(), hand.can_split)
                    print(player_input)
                    # Stick
                    if player_input == 's':
                        hand.finished = True
                        hand_count += 1
                        show_hands(hands,hand_count)
                    # Hit
                    if player_input == 'h':
                        hand.draw_card()
                    # Double Down
                    elif player_input == 'd':
                        hand.draw_card()
                        hand.score = hand.score * 2
                        hand.finished = True
                        hand_count += 1
                    # Split
                    elif player_input == 'sp':
                        split_count += 1
                        print('MFSPLIT')

                        if hand.can_split:
                            hands_played = 0
                            hand_count = 0
                            split_hand(hand,split_count)
                            '''if not you2.inplay:
                                you2 = player(True)
                                you2.cards.append(hand.split())
                                you2.draw_card()
                                hand.draw_card()
                                hands.append(you2)
                            elif not you3.inplay:
                                you3 = player(True)
                                you3.cards.append(hand.split())
                                you3.draw_card()
                                hand.draw_card()
                                hands.append(you3)
                            elif not you4.inplay:
                                you4 = player(True)
                                you4.cards.append(hand.split())
                                you4.draw_card()
                                hand.draw_card()
                                hands.append(you4)'''

                    show_hands(hands,hand_count)

                    if is_bust(hand,hands):
                        hand.finished = True
                        your_score += hand.score
                        hand_count += 1

        # Dealers Turn
        if not game_over:
            while not dealers_go_over:
                # Checking if dealer has soft 17 then must hit
                if dealer.check_soft():
                    if dealer.total == 17:
                        dealer.draw_card()
                if dealer.total < 17:
                    dealer.draw_card()
                else:
                    if dealer.check_bust():
                        if len(hands) != 0:
                            print(f'Dealer has: ', end="")
                            for card in dealer.cards:
                                print(f'[{card.name}]', end=" ")
                            print(f'\nTotal: {dealer.total}')
                            print('YOU WIN - Dealer has gone bust.')
                            your_score += you.score
                            game_over = True
                    dealers_go_over = True
            # Reveal the Dealers Cards
            print(f'Dealer has: ', end="")
            for card in dealer.cards:
                print(f'[{card.name}]', end=" ")
            print(f' Total: {dealer.total}')

        # Calculate the winner and adjust the scores
        if not game_over:
            for hand in hands:
                if dealer.total > hand.total:
                    print('DEALER WINS')
                    hand.score = -hand.score
                    #your_score -= hand.score
                elif dealer.total < hand.total:
                    print('YOU WIN')
                elif dealer.total == hand.total:
                    print('DRAW')
                    hand.score = 0
                your_score += hand.score
                print(hand," : ",hand.score)

        print(your_score_tot.append(your_score))
        game_score = your_score_tot[-1] - your_score_tot[-2]
        print('profit = ',game_score)
        print(f'{line}\n          Your Score: ({your_score})\n{line}\n')

        #time.sleep(0.0000001)
        input('New hand?')
        x += 1

        training_data.append((game_memory, game_score))

    if game_score >= 0:
        accepted_scores.append(game_score)


    return your_score

def neural_network_model(input_size):
    network = input_data(shape = [None, input_size, 1], name='input')

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 512, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 4, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

    model = tflearn.DNN(network,tensorboard_dir='log')

    return model

def train_model(training_data, model=False):
    x = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]), 1)
    y = [i[1] for i in training_data]

    if not model:
        model = neural_network_model(len(x[0]))

    model.fit({'input':x},{'targets':y}, n_epoch=5, snapshot_step=500, show_metric=True, run_id='openaistuff')

    return model




game(5)
#enablePrint()
#training_data[game_number][0=turns, 1=SCORE][turn_number][0=observations, 1=action]
print(training_data)
#model = train_model(training_data)




House_Edge = -your_score_tot[-1]/len(your_score_tot)

'''with open('Game_data.txt', 'w+') as f:
    f.write(your_score_tot)
    f.close'''

'''print('House Edge = ',House_Edge)
print('Number of Splits = ', split_count)
plt.plot(your_score_tot)
plt.show()'''



