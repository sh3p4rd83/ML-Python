class Deck:
    def __init__(self):
        self.cards = self.default()

    def default(self):
        return {
            "F": 16,
            "A": 4,
            "2": 4,
            "3": 4,
            "4": 4,
            "5": 4,
            "6": 4,
            "7": 4,
            "8": 4,
            "9": 4,
        }

    def count_cards(self):
        count = 0
        for card in self.cards:
            count += self.cards[card]
        return count

    def reset(self):
        self.cards = self.default()

    def remove_card(self, card):
        if card in ["K", "Q", "J", "10"]:
            card = "F"

        self.cards[card] -= 1

    def print_deck(self):
        score = 0
        for card in self.cards:
            if card == "F":
                score += (10 * self.cards[card])
            elif card == "A":
                score += (11 * self.cards[card])
            else:
                score += (int(card) * self.cards[card])
        return score
