import unittest

from xcell import CellConstraint, Matcher


class TestCellConstraint(unittest.TestCase):
    def setUp(self):
        self.message = 'Error'

        def validate(arg):
            if arg == 1:
                return True
            else:
                return False

        self.simple_validate = validate
        self.matcher = Matcher(validate)
        self.constraint = CellConstraint(self.message, matchers=[self.matcher])

    def test_cell_constraint_gives_correct_message_if_invalid(self):
        self.assertEquals(self.message, self.constraint(None))

    def test_cell_constraint_gives_no_message_if_valid(self):
        self.assertEquals('', self.constraint(1))

    def test_constraint_fails_if_one_matcher_passes_one_fails(self):
        def validate_2(arg):
            if arg != 1:
                return True
            else:
                return False
        matcher2 = Matcher(validate_2)
        constraint2 = CellConstraint(self.message,
                                     matchers=[self.matcher, matcher2])
        self.assertEquals(self.message, constraint2(1))
