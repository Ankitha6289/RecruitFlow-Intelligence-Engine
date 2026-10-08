import unittest
from unittest.mock import MagicMock, patch
from app import create_app
from app.services.dashboard_service import DashboardService

class DashboardServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True

    @patch('app.services.dashboard_service.db.session')
    @patch('app.services.dashboard_service.Candidate')
    @patch('app.services.dashboard_service.Skill')
    @patch('app.services.dashboard_service.AIAnalysis')
    @patch('app.services.dashboard_service.User')
    @patch('app.services.dashboard_service.Interview')
    @patch('app.services.dashboard_service.Job')
    @patch('app.services.dashboard_service.Offer')
    def test_get_dashboard_data_returns_serializable_top_skills(
        self, mock_offer, mock_job, mock_interview, mock_user, mock_ai_analysis, mock_skill, mock_candidate, mock_db_session
    ):
        # Setup mocks for counts and scalar calls
        mock_candidate.query.count.return_value = 5
        mock_skill.query.count.return_value = 10
        mock_ai_analysis.query.count.return_value = 8
        mock_user.query.filter_by.return_value.count.return_value = 3
        mock_job.query.count.return_value = 4
        mock_interview.query.count.return_value = 6
        mock_offer.query.count.return_value = 2

        mock_interview.query.filter_by.return_value.count.return_value = 1
        mock_offer.query.filter_by.return_value.count.return_value = 1

        mock_db_session.query.return_value.scalar.return_value = 85.5

        # Setup mock for top_skills query
        class MockRow:
            def __init__(self, skill, count):
                self.skill_name = skill
                self.count = count
            def __getitem__(self, index):
                if index == 0:
                    return self.skill_name
                elif index == 1:
                    return self.count
                raise IndexError

        mock_rows = [MockRow("Python", 5), MockRow("Flask", 3)]

        mock_query_chain = MagicMock()
        mock_query_chain.group_by.return_value.order_by.return_value.limit.return_value.all.return_value = mock_rows
        mock_db_session.query.return_value = mock_query_chain

        # Call get_dashboard_data
        with self.app.app_context():
            data = DashboardService.get_dashboard_data()

        # Assert top_skills returns list of standard tuples, not Row/MockRow objects
        self.assertEqual(data["top_skills"], [("Python", 5), ("Flask", 3)])
        # Check that it's json serializable
        import json
        serialized = json.dumps(data["top_skills"])
        self.assertEqual(serialized, '[["Python", 5], ["Flask", 3]]')

if __name__ == '__main__':
    unittest.main()
