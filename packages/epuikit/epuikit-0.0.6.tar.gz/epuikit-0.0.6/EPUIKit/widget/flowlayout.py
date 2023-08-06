from EPUIKit.utils import Dimension
from EPUIKit.widget.layout import Layout


class FlowLayout(Layout):
    def __init__(self, gap=0, padding=0, border=0):
        super().__init__(gap, padding, border)
        self.widgets = list()

    def add(self, widget):
        self.widgets.append(widget)
        return self

    def paint(self, canvas, d):
        super().paint(canvas, d)
        border = self.padding + self.border
        for i, widget in enumerate(self.widgets):
            if widget is not None:
                size = widget.font.size
                widget.paint(canvas, Dimension(d.x + border,
                                               d.y + (size + self.gap) * i + border,
                                               size,
                                               d.width))
