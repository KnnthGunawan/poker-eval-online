import eval7

def calculate_hand_equity(hand, num_opponents=1, simulations=10000):
    deck = eval7.Deck()

    #Remove player's hand from the deck
    for card in hand:
        deck.cards.remove(card)

    wins = 0

    #Run simulations
    for i in range(simulations):
        #If not enough cards left in deck, reshuffle it
        if len(deck.cards) < (num_opponents * 2 + 5):
            deck = eval7.Deck()
            for card in hand:
                deck.cards.remove(card)
        
        deck.shuffle()  #Shuffle the deck for each simulation

        #Deal hands for the opponents
        opponent_hands = [deck.deal(2) for i in range(num_opponents)]

        #Deal the community cards (flop, turn, river)
        community_cards = deck.deal(5)

        #Evaluate the player's hand with community cards
        player_hand_strength = eval7.evaluate(hand + community_cards)

        #Evaluate the opponent's hands with community cards
        opponent_wins = True
        for opponent_hand in opponent_hands:
            opponent_hand_strength = eval7.evaluate(opponent_hand + community_cards)
            if opponent_hand_strength < player_hand_strength:
                opponent_wins = False
                break

        if not opponent_wins:
            wins += 1

    #Calculate the equity as the win percentage
    equity = (wins / simulations) * 100
    return equity

# hand = [eval7.Card('2s'), eval7.Card('7d')]  
# equity = calculate_hand_equity(hand, num_opponents=1, simulations=1000)
# print(f"Estimated equity: {equity:.2f}%")

# hand = [eval7.Card('As'), eval7.Card('Ad')]  
# equity = calculate_hand_equity(hand, num_opponents=1, simulations=1000)
# print(f"Estimated equity: {equity:.2f}%")
