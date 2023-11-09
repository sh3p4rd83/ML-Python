class GameData:
    """
    Store and use game datas for monitoring.
    """

    def __init__(self,total_games_played, session_games_played, wins, loses):
        self.total_games_played = total_games_played
        self.session_games_played = session_games_played
        self.wins = wins
        self.loses = loses

    def play_game(self):
        """
        The number of games played
        """
        self.total_games_played += 1
        self.session_games_played += 1

    def lose_game(self):
        """
        The number of lost games
        """
        self.loses += 1

    def win_game(self):
        """
        The number of won games
        """
        self.wins += 1

    def get_game_data(self):
        """
        Format the game data into an array
        :return: Game Data
        """
        return [self.total_games_played, self.session_games_played, self.wins, self.loses]

    def __str__(self):
        return f"Session games played: {self.session_games_played}, won: {self.wins}, lose: {self.loses}"
