from StringIO import StringIO
import unittest
import xlsxwriter
from xcell import (
    Cell, CELL_TYPES, Location, Workbook, InvalidCellType, InvalidCellLocation
)
from xcell.read import xlrd_reader


class TestCell(unittest.TestCase):
    def test_when_only_location_differs_two_cells_should_be_equal(self):
        actual = Cell('foo', CELL_TYPES[1], Location('bar', 0, 0))
        expected = Cell('foo', CELL_TYPES[1], Location('baz', 1, 1))

        self.assertEqual(expected, actual)

    def test_cell_datatype_should_be_one_of_cell_types(self):
        for t in CELL_TYPES:
            cell = Cell('foo', t, Location('bar', 0, 0))

        with self.assertRaises(InvalidCellType):
            cell = Cell('foo', 'bobbins', Location('bar', 0, 0))

        del cell


class TestLocation(unittest.TestCase):
    def test_when_representative_of_same_location_should_be_equal(self):
        actual = Location('foo', 0, 0)
        expected = Location('foo', 0, 0)

        self.assertEqual(expected, actual)

    def test_a_sheet_should_be_a_string(self):
        loc = Location('name', 0, 0)

        with self.assertRaises(InvalidCellLocation):
            loc = Location(0, 0, 0)

        del loc

    def test_row_and_col_should_be_ints_valued_zero_or_more(self):
        loc = Location('name', 0, 0)

        with self.assertRaises(InvalidCellLocation):
            loc = Location('name', -1, 0)

        with self.assertRaises(InvalidCellLocation):
            loc = Location('name', 0, -1)

        del loc


class FakeReader(object):
    def __init__(self, sheet_names, cells):
        self.sheet_names = sheet_names
        self.cells = cells

    def __call__(self, f):
        d = {}
        for sheet in self.sheet_names:
            d[sheet] = {}
            for cell in filter(lambda c: c.location.sheet == sheet,
                               self.cells):
                d[sheet][(cell.location.row, cell.location.col)] = cell

        return d


class TestWorkbook(unittest.TestCase):
    def setUp(self):
        self.sheet_names = ('foo', 'bar')
        self.f = StringIO()
        self.reader = FakeReader(self.sheet_names, [])
        self.cell_location = Location(self.sheet_names[0], 0, 0)
        self.cell = Cell('baz', CELL_TYPES[1], self.cell_location)

    def test_should_make_the_sheet_names_available(self):
        actual = Workbook(self.f, self.reader).sheet_names()
        expected = self.sheet_names

        self.assertEqual(expected, actual)

    def test_should_make_each_cell_available(self):
        self.reader.cells.append(self.cell)
        actual = Workbook(self.f, self.reader).get(self.cell_location)
        expected = self.cell

        self.assertEqual(expected, actual)


class TestXlrdReader(unittest.TestCase):
    def setUp(self):
        self.f = StringIO()
        self.workbook = xlsxwriter.Workbook(self.f)

    def test_returned_data_should_be_immutable(self):
        worksheet = self.workbook.add_worksheet('foo')
        worksheet.write('A1', 'cell_contents')
        self.workbook.close()
        data = xlrd_reader(self.f)

        with self.assertRaises(NotImplementedError):
            data['bar'] = {}

    def test_workbook_and_reader_should_be_compatible(self):
        self.workbook.add_worksheet('foo')
        self.workbook.close()

        book = Workbook(self.f, xlrd_reader)

        self.assertEqual(('foo',), book.sheet_names())
        self.assertEqual(0, len(book.sheets['foo'].values()))
