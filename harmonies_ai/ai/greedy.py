from random import choice
from harmonies_ai.game_state import GameState


def simulate_game(gs: GameState):
    while not gs.game_ended:
        tokens = choice(gs.display_tokens)
        for token in tokens:
            next_states = [
                gs.copy().place_token(token, pos)
                for pos, stack in enumerate(gs.board)
                if token in stack.placements
            ]
            gs = max(next_states, key=lambda s: s.score.total)
        gs.end_turn()
    return gs
