import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app import create_app
from app.services.candidate_status_service import CandidateStatusService


class CandidateStatusServiceTestCase(unittest.TestCase):
    def test_update_status_sends_email_for_selected_status(self):
        app = create_app()
        app.config['TESTING'] = True

        with app.app_context():
            candidate = SimpleNamespace(candidate_id=1, status='Applied', email='user@example.com')

            with patch('app.services.candidate_status_service.Candidate.query.get', return_value=candidate), \
                 patch('app.services.candidate_status_service.db.session.commit'), \
                 patch('app.services.candidate_status_service.EmailService.selection_email') as selection_email:
                result = CandidateStatusService.update_status(1, 'Selected')

            self.assertTrue(result)
            selection_email.assert_called_once()


if __name__ == '__main__':
    unittest.main()
