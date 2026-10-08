import unittest
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import patch

from app import create_app


class UploadResumePathTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_upload_route_persists_resume_path(self):
        with self.client.session_transaction() as session:
            session['user_id'] = 1

        dummy_candidate = SimpleNamespace(candidate_id=42)

        with patch('app.routes.upload.ResumeExtractor.extract', return_value='dummy text'), \
             patch('app.routes.upload.ResumeParser') as parser_cls, \
             patch('app.routes.upload.CandidateService.save_complete_candidate', return_value=dummy_candidate) as save_mock:
            parser_cls.return_value.parse.return_value = {
                'full_name': 'Test User',
                'email': 'test@example.com',
                'skills': ['python']
            }

            response = self.client.post(
                '/upload',
                data={'resumes': (BytesIO(b'dummy pdf content'), 'sample.pdf')},
                content_type='multipart/form-data'
            )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(dummy_candidate.resume_path, 'sample.pdf')
        save_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
