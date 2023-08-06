from PIL import ImageDraw

from EPUIKit.widget.widget import Widget


class Label(Widget):
    def __init__(self, text, image=None, image_size=16, font=None, padding=0):
        super().__init__(font, padding)
        self.text = text
        self.image = image
        self.image_size = image_size

    def paint(self, canvas, dimension):
        pen = ImageDraw.Draw(canvas)
        if self.image is not None:
            canvas.paste(self.image, (dimension.x, dimension.y))
            pen.text((dimension.x + self.image_size, dimension.y), self.text, font=self.font, fill=0)
        else:
            pen.text((dimension.x, dimension.y), self.text, font=self.font, fill=0)
