class Message(object):
    def __init__(self, dest, type):
        self.dest = dest
        self.type = type
        self.done = False
        self.msg = None