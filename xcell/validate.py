class Matcher(object):
    def __init__(self, *valid):
        self.valid = valid

    def __call__(self, target):
        for validator in self.valid:
            if not validator(target):
                return False

        return True


Any = Matcher(lambda t: True)


class CellConstraint(object):
    def __init__(self, message, matchers=None):
        self.matchers = [Any] if matchers is None else matchers
        self.message = message

    def _matches(self, results):
        return results == set([True])

    def __call__(self, cell):
        results = set([matcher(cell) for matcher in self.matchers])
        return '' if self._matches(results) else self.message
