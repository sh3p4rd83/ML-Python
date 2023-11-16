
class EtatPartie:
    """
    Set all data for ONE game
    """
    def __init__(self, state, cash):
        self.state = state
        self.cash = cash
        self.dealer_cards = []
        self.player_cards = []

    def sum_player(self):
        """
        calculate sum of player cards
        :return: Player score
        """
        score = 0
        for card in self.player_cards:
            if card == "J" or card == "Q" or card == "K":
                score += 10
            elif card == "A":
                score += 1 # TODO
            else:
                score += int(card)

        return score


    def sum_dealer(self):
        """
        calculate sum of player cards
        :return: Player score
        """
        score = 0
        for card in self.dealer_cards:
            if card == "J" or card == "Q" or card == "K":
                score += 10
            elif card == "A":
                score += 1 #  TODO
            else:
                score += int(card)

        return score

    def clear_partie(self):
        """
        Generate a new card dead
        """
        self.player_cards = []
        self.dealer_cards = []

    def add_dealer_card(self, carte):
        """
        Add a card to dealer hand
        :param carte: The card to add
        """
        self.dealer_cards.append(carte)

    def add_player_card(self, carte):
        """
        Add a card to player hand
        :param carte: The card to add
        """
        self.player_cards.append(carte)

    def str_player_cards(self):
        """
        Stringify player cards
        :return: A string of player card
        """
        string = "( "
        for card in self.player_cards:
            string = string + card + " "
        return string + ")"

    def str_dealer_cards(self):
        """
        Stringify dealer cards
        :return: A string of dealer card
        """
        string = "( "
        for card in self.dealer_cards:
            string = string + card + " "
        return string + ")"

    def is_lose(self):
        """
        Define if player lost session
        :return: boolean of session lost
        """
        return self.cash == 0

    def is_flag(self):
        """
        Define if player got the flag
        :return: boolean of session won
        """
        return self.cash >= 2000

    def __str__(self):
        return (f"Game ended on a {self.state} with player cards" +
                f" being {self.str_player_cards()} and dealer being {self.str_dealer_cards()}")
