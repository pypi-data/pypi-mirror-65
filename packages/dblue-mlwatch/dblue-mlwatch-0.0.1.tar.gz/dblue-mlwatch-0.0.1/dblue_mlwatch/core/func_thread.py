import time

from threading import Thread

from dblue_mlwatch.logger import logger


class FuncThread(Thread):
    def __init__(self, delay, func, *args, **kwargs):
        super(FuncThread, self).__init__()
        self.stopped = False
        self.delay = delay  # Time between calls
        self.func = func
        self.args = args
        self.kwargs = kwargs

        self.start()

    def run(self):
        while not self.stopped:
            # Call the function
            try:
                self.func(*self.args, **self.kwargs)
            except Exception as e:
                logger.exception(e)

            time.sleep(self.delay)

    def stop(self):
        self.stopped = True
