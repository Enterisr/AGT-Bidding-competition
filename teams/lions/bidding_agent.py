"""
AGT Competition - Student Agent Template
========================================

Team Name: lions
Members:
  - Aminadav Eliyahu 209289375
  - Or Israeli 208311365
  - Yedaaya Zivan 322409624

Strategy Description:
We calculate how much budget to "waste" per round based on remaining budget
and rounds left, then bid a portion of the item's value. After running many
test games we tuned the aggressiveness parameter to get the best average results.

Key Features:
- Budget-aware bidding that adjusts based on rounds remaining
- Never bid more than item value (reduce by 1-5% if needed)
- Caps bids at available budget to avoid overspending
"""

import random
from typing import Dict, List

BUDGET_PER_ROUND = 4
# PANIC_BUY_FACTOR = 1.5
# PANIC_BUY_ROUNDS = 2
AGRESSIVENESS = 0.85


class BiddingAgent:

    def __init__(
        self,
        team_id: str,
        valuation_vector: Dict[str, float],
        budget: float,
        opponent_teams: List[str],
    ):
        self.team_id = team_id
        self.valuation_vector = valuation_vector
        self.budget = budget
        self.initial_budget = budget
        self.opponent_teams = opponent_teams
        self.utility = 0
        self.items_won = []

        self.rounds_completed = 0
        self.total_rounds = 15

    def _update_available_budget(
        self, item_id: str, winning_team: str, price_paid: float
    ):
        if winning_team == self.team_id:
            self.budget -= price_paid
            self.items_won.append(item_id)

    def update_after_each_round(
        self, item_id: str, winning_team: str, price_paid: float
    ):
        self._update_available_budget(item_id, winning_team, price_paid)

        if winning_team == self.team_id:
            self.utility += self.valuation_vector[item_id] - price_paid

        self.rounds_completed += 1

        return True

    def bidding_function(self, item_id: str) -> float:
        my_valuation = self.valuation_vector.get(item_id, 0)

        if my_valuation <= 0 or self.budget <= 0:
            return 0.0

        rounds_remaining = self.total_rounds - self.rounds_completed

        waste_factor = (self.budget / rounds_remaining) / BUDGET_PER_ROUND
        print(f"budget: {self.budget}")
        print(f"rounds_remaining: {rounds_remaining}")

        # if rounds_remaining <= PANIC_BUY_ROUNDS:
        #     waste_factor += PANIC_BUY_FACTOR

        bid = waste_factor * my_valuation * AGRESSIVENESS
        print(f"factor: {waste_factor}")
        print(f"valuation: {my_valuation}")
        if bid > my_valuation:
            print(f"detected bid is bigger than value")
            deduction_percentage = random.uniform(0.01, 0.2)
            bid = my_valuation * (1 - deduction_percentage)

        if bid > self.budget:
            bid = self.budget

        if bid < 0:
            bid = 0.0

        return float(bid)
