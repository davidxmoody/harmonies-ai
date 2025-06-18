from rich.text import Text
from harmonies_ai.tokens import Token


Pixel = str | Token | Text


def format_pixel(pixel: Pixel):
    if isinstance(pixel, Text):
        return pixel
    if isinstance(pixel, Token):
        pixel = pixel.bg
    return Text(" ", style=f"on {pixel}")


class RichCanvas:
    origin: int
    pixels: dict[tuple[int, int], Pixel]

    def __init__(self):
        self.origin = 0
        self.pixels = {}

    def advance_origin(self, extra_space: int):
        y_max = max((y for y, _ in self.pixels), default=0)
        self.origin = y_max + 1 + extra_space

    def draw_pixel(self, pos: tuple[int, int], pixel: Pixel):
        y, x = pos[0] + self.origin, pos[1]
        self.pixels[(y, x)] = pixel

    def draw_rect(self, pos: tuple[int, int], size: tuple[int, int], pixel: Pixel):
        y_start, x_start = pos[0], pos[1]
        height, width = size[0], size[1]

        for y in range(y_start, y_start + height):
            for x in range(x_start, x_start + width):
                self.draw_pixel((y, x), pixel)

    def draw_template(
        self, pos: tuple[int, int], template: list[str], labels: dict[str, Pixel]
    ):
        for y, line in enumerate(template):
            for x, char in enumerate(line):
                if char in labels:
                    self.draw_pixel((pos[0] + y, pos[1] + x), labels[char])
                elif char.lower() in labels:
                    self.draw_pixel((pos[0] + y, pos[1] + x), labels[char.lower()])

    def draw_text(self, pos: tuple[int, int], text: str, bg: str, fg: str):
        for x, char in enumerate(text):
            self.draw_pixel((pos[0], pos[1] + x), Text(char, style=f"{fg} on {bg}"))

    def __rich__(self):
        y_range = range(0, max(y for y, _ in self.pixels) + 1)
        x_range = range(0, max(x for _, x in self.pixels) + 1)

        return Text("\n").join(
            Text.assemble(
                *(
                    (
                        format_pixel(self.pixels[(y, x)])
                        if (y, x) in self.pixels
                        else " "
                    )
                    for x in x_range
                )
            )
            for y in y_range
        )
