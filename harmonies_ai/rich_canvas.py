from rich.text import Text


class RichCanvas:
    origin: int
    pixels: dict[tuple[int, int], str]

    def __init__(self):
        self.origin = 0
        self.pixels = {}

    def advance_origin(self):
        y_max = max(y for y, _ in self.pixels)
        self.origin = y_max + 2

    def draw(self, color: str, pos: tuple[int, int]):
        y, x = pos[0] + self.origin, pos[1]
        self.pixels[(y, x)] = color

    def fill(
        self, color: str, top_left: tuple[int, int], height_width: tuple[int, int]
    ):
        y_start, x_start = top_left[0], top_left[1]
        height, width = height_width[0], height_width[1]

        for y in range(y_start, y_start + height):
            for x in range(x_start, x_start + width):
                self.draw(color, (y, x))

    def __rich__(self):
        y_range = range(0, max(y for y, _ in self.pixels) + 1)
        x_range = range(0, max(x for _, x in self.pixels) + 1)

        return Text("\n").join(
            Text.assemble(
                *(
                    (
                        Text(" ", style=f"on {self.pixels[(y, x)]}")
                        if (y, x) in self.pixels
                        else " "
                    )
                    for x in x_range
                )
            )
            for y in y_range
        )
