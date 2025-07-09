from harmonies_ai.game_state import GameState
from harmonies_ai.tokens import Token
from itertools import product


# TODO maybe move into the enum itself
_placement_priority = [
    Token.GRY,
    Token.BRN,
    Token.RED,
    Token.GRN,
    Token.BLU,
    Token.YLW,
]


def sort_by_placement_priority(tokens: tuple[Token, ...]):
    return tuple(sorted(tokens, key=lambda t: _placement_priority.index(t)))


def has_conflict(gs: GameState, turn: tuple[tuple[Token, int]]):
    updated_stacks = {}
    for token, pos in turn:
        stack = updated_stacks.get(pos, gs.board[pos])
        if token not in stack.placements:
            return True
        updated_stacks[pos] = stack.placements[token]


def get_next_states(gs: GameState):
    token_spots = {
        token: tuple(
            pos
            for pos, stack in enumerate(gs.board)
            if token in stack.placements and not gs.cubes[pos]
        )
        for token in Token
    }

    turns = set()

    for tokens in set(gs.display_tokens):
        sorted_tokens = sort_by_placement_priority(tokens)
        turns.update(
            product(
                *[
                    [(token, pos) for pos in token_spots[token]]
                    for token in sorted_tokens
                ]
            )
        )

    for turn in turns:
        if not has_conflict(gs, turn):
            yield gs.copy().place_token(*turn[0]).place_token(*turn[1]).place_token(
                *turn[2]
            )


def simulate_game(gs: GameState):
    while not gs.game_ended:
        next_states = get_next_states(gs)
        gs = max(next_states, key=lambda s: s.score.total)
        gs.end_turn()
    return gs
