import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from app import create_app
from app.services.candidate_service import CandidateService


class CandidateServiceDeduplicationTestCase(unittest.TestCase):
    def test_save_candidate_updates_existing_candidate_on_duplicate_email(self):
        app = create_app()
        app.config['TESTING'] = True

        with app.app_context():
            existing_candidate = SimpleNamespace(
                candidate_id=7,
                full_name="Old Name",
                email="dupe@example.com",
                phone=None,
                linkedin=None,
                github=None,
                portfolio=None,
                address=None,
                status="Applied",
                password="old"
            )

            mock_query = Mock()
            mock_query.filter_by.return_value.first.return_value = existing_candidate

            with patch('app.services.candidate_service.Candidate.query', mock_query), \
                 patch('app.services.candidate_service.ActivityLogService.create'), \
                 patch('app.services.candidate_service.NotificationService.create'), \
                 patch('app.services.candidate_service.db.session.commit') as commit_mock:
                result = CandidateService.save_candidate({
                    'email': 'dupe@example.com',
                    'full_name': 'Updated Name',
                    'phone': '123456',
                    'linkedin': 'https://linkedin.com/in/example',
                    'github': 'https://github.com/example',
                    'portfolio': 'https://example.com',
                    'address': 'New York'
                })

            self.assertIs(result, existing_candidate)
            self.assertEqual(existing_candidate.full_name, 'Updated Name')
            self.assertEqual(existing_candidate.phone, '123456')
            self.assertEqual(existing_candidate.address, 'New York')
            commit_mock.assert_called_once()



if __name__ == '__main__':
    unittest.main()
