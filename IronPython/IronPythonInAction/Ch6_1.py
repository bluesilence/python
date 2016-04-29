class PropertyExample(object):
    def __init__(self, x):
        self._x = x

    def _getX(self):
        print "getting x"
        return self._x

    def _setX(self, value):
        print "setting x"
        self._x = value

    def _delX(self):
        print "Attempting to delete x"

    x = property(_getX, _setX, _delX)
