from PySide6.QtCore import QRunnable, Signal, Slot, QThreadPool

'''
This is a thread, the function, signals to output to and data
'''


class LookupThread(QRunnable):
    def __init__(self, fn, signal, data, *args, **kwargs):
        super(LookupThread, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.data = data
        self.args = args
        self.kwargs = kwargs
        self.signal: Signal = signal

    @Slot()
    def run(self):
        self.fn(self.data, self.signal)
        # print(output)


'''
this is a static class that makes sure all the files in /UI have access to the same 
QThreadPool object (as there can only be one of those per project)
'''


class Thread:
    thread = QThreadPool()

    @staticmethod
    def create_thread(signal: Signal, function, data):
        th = LookupThread(function, signal, data)
        Thread.thread.start(th)

    @staticmethod
    def use_thread(th_class):
        th = th_class()
        Thread.thread.start(th)
