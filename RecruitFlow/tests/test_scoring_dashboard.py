import unittest
from types import SimpleNamespace

from app.services.candidate_management_service import CandidateManagementService


class CandidateScoringDashboardTestCase(unittest.TestCase):
    def test_build_scoring_dashboard_data_aggregates_ai_and_ats_scores(self):
        candidate = SimpleNamespace(
            candidate_id=1,
            full_name='Alice',
            email='alice@example.com',
            analysis=[SimpleNamespace(suitability_scores='88')],
            ats_analysis=[SimpleNamespace(ats_score=76)]
        )

        data = CandidateManagementService.build_scoring_dashboard_data([candidate])

        self.assertEqual(data['total_candidates'], 1)
        self.assertEqual(data['average_score'], 82.0)
        self.assertEqual(data['top_candidates'][0]['overall_score'], 82.0)
        self.assertEqual(data['top_candidates'][0]['candidate'].full_name, 'Alice')


if __name__ == '__main__':
    unittest.main()
