import random
from typing import Dict, List, Tuple

class LudoGame:
    def __init__(self, players: List[int], win_condition: int):
        self.players = {player_id: {'tokens': [-1, -1, -1, -1], 'color': color}
                        for player_id, color in zip(players, ['🔴', '🟢', '🟡', '🔵'])}
        self.win_condition = win_condition
        self.board_path = self._create_board_path()
        self.safe_zones = [0, 8, 13, 21, 26, 34, 39, 47]
        self.current_player_index = 0
        self.dice_roll = 0
        self.consecutive_sixes = 0

    def _create_board_path(self) -> List[int]:
        return list(range(52))

    def roll_dice(self) -> int:
        self.dice_roll = random.randint(1, 6)
        if self.dice_roll == 6:
            self.consecutive_sixes += 1
            if self.consecutive_sixes == 3:
                self.consecutive_sixes = 0
                return -1  # Indicates turn loss
        else:
            self.consecutive_sixes = 0
        return self.dice_roll

    def get_movable_tokens(self, player_id: int, dice_roll: int) -> List[int]:
        movable = []
        player_tokens = self.players[player_id]['tokens']
        for i, pos in enumerate(player_tokens):
            if pos == -1 and dice_roll == 6:
                movable.append(i)
            elif pos != -1:
                movable.append(i)
        return movable

    def move_token(self, player_id: int, token_index: int, dice_roll: int) -> str:
        current_pos = self.players[player_id]['tokens'][token_index]
        if current_pos == -1 and dice_roll == 6:
            self.players[player_id]['tokens'][token_index] = self._get_start_pos(player_id)
            return "entered"

        new_pos = (current_pos + dice_roll) % 52

        # Knockout logic
        for opponent_id, opponent_data in self.players.items():
            if opponent_id != player_id:
                for opp_token_idx, opp_pos in enumerate(opponent_data['tokens']):
                    if opp_pos == new_pos and new_pos not in self.safe_zones:
                        self.players[opponent_id]['tokens'][opp_token_idx] = -1

        self.players[player_id]['tokens'][token_index] = new_pos
        return "moved"

    def _get_start_pos(self, player_id: int) -> int:
        player_ids = list(self.players.keys())
        player_index = player_ids.index(player_id)
        return player_index * 13

    def check_win(self, player_id: int) -> bool:
        home_tokens = sum(1 for pos in self.players[player_id]['tokens'] if pos >= 52)
        return home_tokens >= self.win_condition

    def get_next_player(self) -> int:
        if self.dice_roll != 6:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return list(self.players.keys())[self.current_player_index]

    def get_state(self) -> Dict:
        return {
            'players': self.players,
            'current_player_index': self.current_player_index,
            'dice_roll': self.dice_roll,
        }