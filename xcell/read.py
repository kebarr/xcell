import xlrd
from pysistence import make_dict


CELL_TYPES = ('EMPTY', 'TEXT', 'NUMBER', 'DATE', 'BOOLEAN', 'ERROR', 'BLANK')


class InvalidWorkbook(Exception):
    pass


def xlrd_reader(f):
    """Parse an excel workbook using xlrd into an immutable dict
    """
    f.seek(0)
    data = f.read()
    if data == '':
        raise InvalidWorkbook('Empty')
    sheets = {}
    book = xlrd.open_workbook(file_contents=data)
    for name in book.sheet_names():
        sheet = book.sheet_by_name(name)
        sheets[name] = {}
        for row in range(sheet.nrows):
            for col in range(sheet.nrows):
                raw = sheet.cell(row, col)
                sheets[name][(row, col)] = Cell(
                    raw.value, CELL_TYPES[raw.ctype], Location(name, row, col))

    return make_dict(sheets)


class InvalidCellLocation(Exception):
    pass


class Location(object):
    """Represents the location within a workbook of a cell
    """
    def __init__(self, sheet, row, col):
        if type(sheet) not in (str, unicode):
            raise InvalidCellLocation
        if not isinstance(row, int) or row < 0:
            raise InvalidCellLocation
        if not isinstance(col, int) or col < 0:
            raise InvalidCellLocation
        self.sheet = sheet
        self.row = row
        self.col = col

    def __eq__(self, other):
        if self.sheet == other.sheet:
            if (self.row, self.col) == (other.row, other.col):
                return True

        return False


class InvalidCellType(Exception):
    pass


class Cell(object):
    """Represents a cell in a workbook
    """
    def __init__(self, contents, datatype, location):
        if datatype not in CELL_TYPES:
            raise InvalidCellType
        self.contents = contents
        self.datatype = datatype
        self.location = location

    def __eq__(self, other):
        try:
            if self.datatype == other.datatype:
                if self.contents == other.contents:
                    return True
        except:
            pass

        return False


class Workbook(object):
    """Represent a workbook
    """
    def __init__(self, f, reader):
        self.sheets = reader(f)

    def get(self, location):
        """Return the contents of a cell
        """
        return self.sheets[location.sheet][(location.row, location.col)]

    def sheet_names(self):
        """Show the names of the sheets in the workbook
        """
        return tuple(self.sheets.keys())
