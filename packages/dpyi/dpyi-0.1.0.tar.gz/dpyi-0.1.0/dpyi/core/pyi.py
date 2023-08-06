class PYI(object):

    I = False

    @staticmethod
    def _root(self):
        return self
    
    @staticmethod
    def _extends(self):
        return self

    @staticmethod
    def _runtime(self):
        if PYI.I == False:
            PYI.I = self()
        return PYI.I