from rich.text import Text
from enum import IntFlag, auto


class Token(IntFlag):
    GRAY = auto()
    RED = auto()
    BROWN = auto()
    GREEN = auto()
    BLUE = auto()
    YELLOW = auto()

    def __rich__(self):
        match self:
            case Token.GRAY:
                return Text("GRY", style="#BAC1C5 on #878886")
            case Token.RED:
                return Text("RED", style="#F07A65 on #BA3245")
            case Token.BROWN:
                return Text("BRN", style="#D39C80 on #8B5539")
            case Token.GREEN:
                return Text("GRN", style="#BBD56A on #919627")
            case Token.BLUE:
                return Text("BLU", style="#6AC6D3 on #007A85")
            case Token.YELLOW:
                return Text("YLW", style="#F2EB60 on #D8A705")


class Stack(IntFlag):
    EMPTY = auto()

    MOUNTAIN_1 = auto()
    BUILDING_1 = auto()
    TRUNK_1 = auto()
    TREE_1 = auto()
    WATER_1 = auto()
    FIELD_1 = auto()

    MOUNTAIN_2 = auto()
    BUILDING_2 = auto()
    TRUNK_2 = auto()
    TREE_2 = auto()

    MOUNTAIN_3 = auto()
    TREE_3 = auto()


placements: dict[Stack, dict[Token, Stack]] = {
    Stack.EMPTY: {
        Token.GRAY: Stack.MOUNTAIN_1,
        Token.RED: Stack.BUILDING_1,
        Token.BROWN: Stack.TRUNK_1,
        Token.GREEN: Stack.TREE_1,
        Token.BLUE: Stack.WATER_1,
        Token.YELLOW: Stack.FIELD_1,
    },
    Stack.MOUNTAIN_1: {
        Token.GRAY: Stack.MOUNTAIN_2,
        Token.RED: Stack.BUILDING_2,
    },
    Stack.BUILDING_1: {
        Token.RED: Stack.BUILDING_2,
    },
    Stack.TRUNK_1: {
        Token.RED: Stack.BUILDING_2,
        Token.BROWN: Stack.TRUNK_2,
        Token.GREEN: Stack.TREE_2,
    },
    Stack.MOUNTAIN_2: {
        Token.GRAY: Stack.MOUNTAIN_3,
    },
    Stack.TRUNK_2: {
        Token.GREEN: Stack.TREE_3,
    },
}


def _find_compatible(stack: Stack):
    result = stack
    for before, after in placements.items():
        if stack in after.values():
            result |= _find_compatible(before)
    return result


compatibility: dict[Stack, Stack] = {s: _find_compatible(s) for s in Stack}
