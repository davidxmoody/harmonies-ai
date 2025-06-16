from rich.text import Text
from enum import Enum


class Token(Enum):
    bg: str
    fg: str

    GRY = ("#878886", "#BAC1C5")
    RED = ("#BA3245", "#F07A65")
    BRN = ("#8B5539", "#D39C80")
    GRN = ("#919627", "#BBD56A")
    BLU = ("#007A85", "#6AC6D3")
    YLW = ("#D8A705", "#F2EB60")

    def __init__(self, bg: str, fg: str):
        self.bg = bg
        self.fg = fg

    def __repr__(self):
        return self.name

    def __rich__(self):
        return Text(self.name, style=f"{self.fg} on {self.bg}")


class Stack(Enum):
    components: tuple[Token, ...]
    alt_components: tuple[tuple[Token, ...], ...]

    EMPTY0 = ((),)

    MOUNT1 = ((Token.GRY,),)
    BUILD1 = ((Token.RED,),)
    TRUNK1 = ((Token.BRN,),)
    TREES1 = ((Token.GRN,),)
    WATER1 = ((Token.BLU,),)
    FIELD1 = ((Token.YLW,),)

    MOUNT2 = ((Token.GRY, Token.GRY),)
    BUILD2 = (
        (Token.RED, Token.RED),
        ((Token.BRN, Token.RED), (Token.GRY, Token.RED)),
    )
    TRUNK2 = ((Token.BRN, Token.BRN),)
    TREES2 = ((Token.BRN, Token.GRN),)

    MOUNT3 = ((Token.GRY, Token.GRY, Token.GRY),)
    TREES3 = ((Token.BRN, Token.BRN, Token.GRN),)

    def __init__(
        self,
        components: tuple[Token, ...],
        alt_components: tuple[tuple[Token, ...], ...] = (),
    ):
        self.components = components
        self.alt_components = alt_components

    def __repr__(self):
        return self.name

    def __rich__(self):
        if len(self.components) == 0:
            return self.name
        return Text(
            self.name, style=f"{self.components[-1].fg} on {self.components[-1].bg}"
        )

    @property
    def placements(self):
        return _placements[self]


_placements: dict[Stack, dict[Token, Stack]] = {
    stack: {
        next_stack.components[-1]: next_stack
        for next_stack in Stack
        if any(
            stack.components == next_components[:-1]
            for next_components in (next_stack.components, *next_stack.alt_components)
        )
        and len(stack.components) == len(next_stack.components) - 1
    }
    for stack in Stack
}


# def _find_compatible(stack: Stack):
#     result = stack
#     for before, after in placements.items():
#         if stack in after.values():
#             result |= _find_compatible(before)
#     return result


# compatibility: dict[Stack, Stack] = {s: _find_compatible(s) for s in Stack}
