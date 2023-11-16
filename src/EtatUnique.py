class EtatUnique:
    """

    """

    def __init__(self, dealer_points, player_points, action, wins=0, loses=0):
        self.dealer_points = dealer_points
        self.player_points = player_points
        self.action = action
        self.wins = wins
        self.loses = loses

    def set_game_status(self, status):
        self.status = status

    def get_game_status(self):
        return [
            self.get_hashed_game_status(),
            self.dealer_points,
            self.player_points,
            self.action,
            self.wins,
            self.loses
        ]

    def get_hashed_game_status(self):
        return hash(f"{self.dealer_points}, {self.player_points}, {self.action}")

    def win(self):
        self.wins += 1

    def lose(self):
        self.loses += 1
