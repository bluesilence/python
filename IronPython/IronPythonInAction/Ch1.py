class ExampleMappingType(object):
    def __init__(self):
        self._dataStore = {}

    def __getitem__(self, key):
        value = self._dataStore[key]
        print 'Fetching: %s, Value is: %s' % (key, value)

        return value

    def __setitem__(self, key, value):
        print 'Setting: %s to %s' % (key, value)
        self._dataStore[key] = value

    def __delitem__(self, key):
        print 'Deleting:', key
        del self._dataStore[key]