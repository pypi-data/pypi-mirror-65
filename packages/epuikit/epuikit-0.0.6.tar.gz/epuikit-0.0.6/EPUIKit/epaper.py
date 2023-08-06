import logging
import sched
import time

from PIL import Image

from EPUIKit.date import is_screen_work_time
from EPUIKit.paper import Paper
from EPUIKit.utils import UILoop, Dimension

logging.basicConfig(level=logging.DEBUG)

MAX = 10


class EPaper(Paper):
    def __init__(self, epd, layout, interval=30):
        super().__init__(layout, epd.height, epd.width)
        self.epd = epd
        self.interval = interval
        self.renderCount = 1
        self.sleep = False
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.mainloop = UILoop()
        self.__partial_render_count__ = 0
        self.__render_count__ = 0

    def show(self):
        self.mainloop.run()
        self.schedule.enter(0, 0, self.__mainloop__, (self.interval,))
        self.schedule.run()

    def __mainloop__(self, inc):
        self.mainloop.add_event(self.paint, ())
        self.schedule.enter(inc, 0, self.__mainloop__, (inc,))

    def paint(self):
        try:
            # 工作时间
            if is_screen_work_time():
                logging.debug("work time")
                if self.renderCount == 1:
                    self.renderCount = MAX
                    self.__paint_by__(self.__render__)
                else:
                    self.renderCount -= 1
                    self.__paint_by__(self.__partial_render__)
                self.epd.sleep()
            # 睡眠中
            elif self.sleep:
                logging.debug("sleeping...")
                pass
            # 准备入睡
            else:
                logging.debug("prepare to sleep")
                self.__paint_by__(self.__render__)
                self.renderCount = 1
                self.sleep = True
                self.epd.sleep()
        except Exception as e:
            logging.error("Exception in mainloop: {}".format(e))
            self.epd.sleep()

    def __paint_by__(self, render):
        image = Image.new('1', (self.height, self.width), 255)
        self.layout.paint(image, Dimension(0, 0, self.width, self.height))
        render(image)

    def __partial_render__(self, image):
        logging.info("partial render...")
        self.epd.init(self.epd.PART_UPDATE)
        self.epd.displayPartial(self.epd.getbuffer(image.transpose(Image.ROTATE_180)))
        self.__partial_render_count__ += 1

    def __render__(self, image):
        logging.info("full render...")
        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.displayPartBaseImage(self.epd.getbuffer(image.transpose(Image.ROTATE_180)))
        self.__render_count__ += 1

    def debug_info(self):
        return "p {} f {}".format(self.__partial_render_count__, self.__render_count__)
