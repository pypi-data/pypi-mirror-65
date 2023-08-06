import time


class DummyConstructor:
    def __init__(self, addr):
        self.addr = addr

    def create(self):
        return None


class DummyInitialiser:
    def __init__(self):
        pass

    def initialise(self, handler, channel):
        return True


class DummyParameter:
    def __init__(self, data, dummy=None):
        self.data = data
        self.dummy = dummy
        self.state = True

    def apply(self, handler, value):
        pass

    def is_settled(self, handler):
        self.state = not self.state
        return self.state


class DummyMeasurement:
    def __init__(self, wait_secs=0, trigger_secs=0, dummy=None):
        self.dummy = dummy
        self.wait_secs = wait_secs
        self.trigger_secs = trigger_secs

    def trigger(self, handler):
        time.sleep(self.trigger_secs)

    def wait(self, handler):
        time.sleep(self.wait_secs)
