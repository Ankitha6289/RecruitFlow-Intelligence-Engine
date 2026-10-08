import unittest

from app.services.ats_service import ATSService


class ATSServiceTestCase(unittest.TestCase):
    def test_build_ats_result_returns_score_and_breakdown(self):
        result = ATSService.build_ats_result(["python", "sql", "git"])

        self.assertEqual(result["ats_score"], 30)
        self.assertEqual(result["matched"], ["python", "sql", "git"])
        self.assertIn("flask", result["missing"])
        self.assertIn("python", result["suggestions"])
        self.assertIn("flask", result["suggestions"])


if __name__ == "__main__":
    unittest.main()
