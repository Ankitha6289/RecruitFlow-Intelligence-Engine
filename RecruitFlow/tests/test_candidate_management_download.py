import unittest

from app import create_app


class CandidateManagementDownloadTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_admin_download_resume_route_redirects_when_candidate_missing(self):
        with self.client.session_transaction() as session:
            session['user_id'] = 1

        response = self.client.get('/admin/candidates/download/999999')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/candidates', response.location)


if __name__ == '__main__':
    unittest.main()
