from EPUIKit.utils import Dimension
from EPUIKit.widget.layout import Layout


class QuadrantsLayout(Layout):
    LEFT_TOP = "LEFT_TOP"
    LEFT_BOTTOM = "LEFT_BOTTOM"
    RIGHT_TOP = "RIGHT_TOP"
    RIGHT_BOTTOM = "RIGHT_BOTTOM"

    def __init__(self, gap=0, padding=0, border=0):
        super().__init__(gap, padding, border)
        self.widgets = {self.LEFT_TOP: None, self.LEFT_BOTTOM: None, self.RIGHT_TOP: None, self.RIGHT_BOTTOM: None}

    def add(self, widget, position):
        if position not in self.widgets:
            raise Exception("position is error")
        else:
            self.widgets[position] = widget
        return self

    def paint(self, canvas, d):
        super().paint(canvas, d)
        border = self.padding + self.border
        sub_height = d.height // 2 - border
        sub_width = d.width // 2 - border
        widgets_point = {
            self.LEFT_TOP: Dimension(border + d.x,
                                     border + d.y,
                                     sub_height,
                                     sub_width),
            self.LEFT_BOTTOM: Dimension(border + d.x,
                                        border + d.y + sub_height,
                                        sub_height,
                                        sub_width),
            self.RIGHT_TOP: Dimension(border + d.x + sub_width,
                                      border + d.y,
                                      sub_height,
                                      sub_width),
            self.RIGHT_BOTTOM: Dimension(border + d.x + sub_width,
                                         border + d.y + sub_height,
                                         sub_height,
                                         sub_width)
        }
        for pos, widget in self.widgets.items():
            if widget is not None:
                widget.paint(canvas, widgets_point[pos])
