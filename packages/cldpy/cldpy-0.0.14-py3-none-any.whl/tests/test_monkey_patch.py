class TestMonkeyPatch(object):

    def find_module(self, fullname, path=None):
        print('Test Monkeypatch: %s, %s' % (fullname, path))
        return None
