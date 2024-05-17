import datetime
import json
import os
import random
import string
import time


class GamificationAndSocialTrading:
    def __init__(self, name, threshold=0.5, quorum=0.1):
        self.name = name
        self.threshold = threshold
        self.quorum = quorum
        self.traders = []
        self.trades = []
        self.leaderboard = []

    def new_trader(self, trader_id, name, balance):
        trader = {
            "id": trader_id,
            "name": name,
            "balance": balance,
            "score": 0,
            "trades": [],
        }
        self.traders.append(trader)
        return trader_id

    def new_trade(self, trader_id, symbol, quantity, price, timestamp):
        trader = next((t for t in self.traders if t["id"] == trader_id), None)
        if trader is None:
            raise ValueError("Invalid trader ID")
        trade = {
            "trader_id": trader_id,
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "timestamp": timestamp,
        }
        self.trades.append(trade)
        trader["trades"].append(trade)

    def calculate_score(self):
        for trader in self.traders:
            trader_score = 0
            for trade in trader["trades"]:
                if trade["quantity"] > 0:
                    trader_score += 1
            trader["score"] = trader_score

    def update_leaderboard(self):
        self.leaderboard = sorted(self.traders, key=lambda x: x["score"], reverse=True)

    def save(self, filename):
        data = {
            "name": self.name,
            "threshold": self.threshold,
            "quorum": self.quorum,
            "traders": self.traders,
            "trades": self.trades,
            "leaderboard": self.leaderboard,
        }
        with open(filename, "w") as f:
            json.dump(data, f)

    def load(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
        self.name = data["name"]
        self.threshold = data["threshold"]
        self.quorum = data["quorum"]
        self.traders = data["traders"]
        self.trades = data["trades"]
        self.leaderboard = data["leaderboard"]

    def add_social_feature(self, trader_id, feature):
        trader = next((t for t in self.traders if t["id"] == trader_id), None)
        if trader is None:
            raise ValueError("Invalid trader ID")
        trader[feature] = True

    def remove_social_feature(self, trader_id, feature):
        trader = next((t for t in self.traders if t["id"] == trader_id), None)
        if trader is None:
            raise ValueError("Invalid trader ID")
        trader[feature] = False

    def enable_gamification(self, enable):
        self.gamification_enabled = enable

    def get_leaderboard(self):
        return self.leaderboard

    def get_trades(self):
        return self.trades

    def get_traders(self):
        return self.traders
