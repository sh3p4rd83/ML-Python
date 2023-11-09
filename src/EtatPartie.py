class EtatPartie:
    def __init__(self, state, cash):
        self.state = state
        self.cash = cash
        self.dealer_cards = []
        self.player_cards = []

    def clear_partie(self):
        self.player_cards = []
        self.dealer_cards = []

    def add_dealer_card(self, carte):
        """

        :param carte:
        """
        self.dealer_cards.append(carte)

    def add_player_card(self, carte):
        """

        :param carte:
        """
        self.player_cards.append(carte)

    def str_player_cards(self):
        """

        :return:
        """
        string = "( "
        for card in self.player_cards:
            string = string + card + " "
        return string + ")"

    def str_dealer_cards(self):
        """

        :return:
        """
        string = "( "
        for card in self.dealer_cards:
            string = string + card + " "
        return string + ")"

    def is_lose(self):
        """

        :return:
        """
        return self.cash == 0

    def is_flag(self):
        """

        :return:
        """
        return self.cash >= 2000

    def __str__(self):
        return (f"Game ended on a {self.state} with player cards" +
                f" being {self.str_player_cards()} and dealer being {self.str_dealer_cards()}")
