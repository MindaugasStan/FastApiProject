import unittest
import datetime


from app.services.services import generateEmployeeEmail, generateEmployeeExperience


class TestServices(unittest.TestCase):
    def test_generateEmployeeEmail(self):
        result = generateEmployeeEmail("name", "lastname", "company")
        self.assertEqual(result, "name.lastname@company.com")

    def test_generateEmployeeExperience(self):
        d = datetime.date(2020, 5, 12)
        result = generateEmployeeExperience(d, 2)
        self.assertEqual(result, 4)
