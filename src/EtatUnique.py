class EtatUnique:
    """
    Etat unique dans lequel une partie peut se retrouver
    """

    def __init__(self, dealer_points, player_points, action, wins=0, loses=0):
        self.dealer_points = dealer_points
        self.player_points = player_points
        self.action = action
        self.wins = wins
        self.loses = loses

    def get_game_status(self):
        """
        Transforme un état en array de données
        :return: Un array de données d'un état unique
        """
        return [
            self.get_hashed_game_status(),
            self.dealer_points,
            self.player_points,
            self.action,
            self.wins,
            self.loses
        ]

    def get_hashed_game_status(self):
        """
        Transforme un état en hash unique pour comparaison et storage
        :return: Hash unique
        """
        return hash(f"{self.dealer_points}, {self.player_points}, {self.action}")

    def win(self):
        """
        Gagne une partie
        """
        self.wins += 1

    def lose(self):
        """
        Perd une partie
        """
        self.loses += 1

    def __str__(self):
        return f"dp: {self.dealer_points}, pp: {self.player_points}, A: {self.action}, W: {self.wins}, L: {self.loses}"
