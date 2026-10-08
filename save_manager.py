import json
import os

class SaveManager:
    def __init__(self):
        self.file = 'player_data.json'
        self.total_coins = None
        self.high_scores = None

        self.load_user_data()

    def load_user_data(self):
        if not os.path.exists(self.file):
            self.total_coins = 0
            self.high_scores = 0
            self.save_user_data()

        with open("player_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            self.total_coins = data['total_coins']
            self.high_scores = data['high_scores']

    def update_user_data(self, coins, high_score):
        self.total_coins = coins
        self.high_scores = high_score if high_score > self.high_scores else self.high_scores

    def get_user_data(self):
        return self.total_coins, self.high_scores

    def save_user_data(self):
        data_to_save = {
            'total_coins': self.total_coins,
            'high_scores': self.high_scores
        }
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)