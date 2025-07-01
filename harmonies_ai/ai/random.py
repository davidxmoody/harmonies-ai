from random import choice
from harmonies_ai.game_state import GameState


def simulate_game(gs: GameState):
    while not gs.game_ended:
        tokens = choice(gs.display_tokens)
        for token in tokens:
            pos = choice(
                [pos for pos, stack in enumerate(gs.board) if token in stack.placements]
            )
            gs.place_token(token, pos)
        gs.end_turn()
    return gs
