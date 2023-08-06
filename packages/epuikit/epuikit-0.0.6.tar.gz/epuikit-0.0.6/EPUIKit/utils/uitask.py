from threading import Thread


class UITask(Thread):

    def __init__(self, loop, target=None, args=(), ui_task=None, ui_args=(), name=None):
        super().__init__()
        self.target = target
        self.ui_task = ui_task
        self.args = args
        self.ui_args = ui_args
        self.loop = loop

    def run(self):
        try:
            if self.target:
                self.target(*self.args)
                self.loop.add_evevt(self.ui_task, self.ui_args)
        finally:
            del self.target, self.args
