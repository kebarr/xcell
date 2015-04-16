from StringIO import StringIO
import unittest

from xcell import Cell, CELL_TYPES, Location, Workbook


class TestCell(unittest.TestCase):
    def test_when_only_location_differs_two_cells_should_be_equal(self):
        actual = Cell('foo', CELL_TYPES[1], Location('bar', 0, 0))
        expected = Cell('foo', CELL_TYPES[1], Location('baz', 1, 1))

        self.assertEqual(expected, actual)


class TestLocation(unittest.TestCase):
    def test_when_representative_of_same_location_should_be_equal(self):
        actual = Location('foo', 0, 0)
        expected = Location('foo', 0, 0)

        self.assertEqual(expected, actual)


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
