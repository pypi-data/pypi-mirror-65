from PIL import Image

from EPUIKit import Paper
from EPUIKit.utils import Dimension


class VirtualPaper(Paper):
    def __init__(self, layout, height, width):
        super().__init__(layout, height, width)
        self.image = Image.new('1', (width, height), 255)

    def paint(self):
        self.layout.paint(self.image, Dimension(0, 0, self.height, self.width))

    def show(self):
        self.paint()
        self.image.show()
