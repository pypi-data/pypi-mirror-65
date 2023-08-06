from PIL import ImageDraw

from EPUIKit.widget.widget import Widget


class Layout(Widget):
    def __init__(self, gap=0, padding=0, border=0):
        super().__init__(padding=padding)
        self.gap = gap
        self.border = border

    def paint(self, canvas, dimension):
        if self.border > 0:
            ImageDraw.Draw(canvas).rectangle([(dimension.x, dimension.y),
                                              (dimension.x + dimension.width - 1, dimension.y + dimension.height - 1)],
                                             outline=0)
