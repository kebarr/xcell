class CellConstraint(object):
    def __init__(self, is_invalid, message):
        self.is_invalid = is_invalid
        self.message = message

    def __call__(self, cell):
        return self.message if self.is_invalid(cell) else ''


def one_of(valid, book, sheet, row, col):
    return book.get(sheet, row, col) in valid
