import unittest
from unittest.mock import patch, Mock
from app import create_app


class ChatbotAuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    @patch('app.routes.chatbot.ChatbotService.ask')
    def test_send_allows_recruiter_for_any_candidate(self, mock_ask):
        dummy_chat = Mock()
        dummy_chat.user_question = "What are their skills?"
        dummy_chat.ai_answer = "Python, Flask"
        mock_ask.return_value = dummy_chat

        with self.client.session_transaction() as session:
            session['user_id'] = 1  # Recruiter/Admin logged in

        response = self.client.post(
            '/chatbot/send',
            json={
                'candidate_id': 42,
                'question': 'What are their skills?'
            }
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['question'], 'What are their skills?')
        self.assertEqual(data['answer'], 'Python, Flask')
        mock_ask.assert_called_once_with(42, 'What are their skills?')

    @patch('app.routes.chatbot.ChatbotService.ask')
    def test_send_allows_candidate_for_own_chatbot(self, mock_ask):
        dummy_chat = Mock()
        dummy_chat.user_question = "What are my skills?"
        dummy_chat.ai_answer = "Python, Flask"
        mock_ask.return_value = dummy_chat

        with self.client.session_transaction() as session:
            session['candidate_id'] = 42  # Candidate logged in

        response = self.client.post(
            '/chatbot/send',
            json={
                'candidate_id': 42,
                'question': 'What are my skills?'
            }
        )

        self.assertEqual(response.status_code, 200)
        mock_ask.assert_called_once_with(42, 'What are my skills?')

    def test_send_blocks_candidate_for_other_chatbot(self):
        with self.client.session_transaction() as session:
            session['candidate_id'] = 42  # Candidate 42 logged in

        response = self.client.post(
            '/chatbot/send',
            json={
                'candidate_id': 99,  # Trying to access candidate 99
                'question': 'What are their skills?'
            }
        )

        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['error'], 'Unauthorized')

    def test_send_blocks_unauthenticated_user(self):
        response = self.client.post(
            '/chatbot/send',
            json={
                'candidate_id': 42,
                'question': 'What are my skills?'
            }
        )

        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['error'], 'Unauthorized')


    def test_view_chatbot_page_renders_successfully_for_recruiter(self):
        with self.app.app_context():
            with patch('app.routes.chatbot.ChatbotHistory.query') as mock_query:
                mock_query.filter_by.return_value.all.return_value = []
                with self.client.session_transaction() as session:
                    session['user_id'] = 1

                response = self.client.get('/chatbot/42')
                self.assertEqual(response.status_code, 200)

    def test_view_chatbot_page_renders_successfully_for_own_candidate(self):
        with self.app.app_context():
            with patch('app.routes.chatbot.ChatbotHistory.query') as mock_query:
                mock_query.filter_by.return_value.all.return_value = []
                with self.client.session_transaction() as session:
                    session['candidate_id'] = 42

                response = self.client.get('/chatbot/42')
                self.assertEqual(response.status_code, 200)

    def test_view_chatbot_page_redirects_for_different_candidate(self):
        with self.client.session_transaction() as session:
            session['candidate_id'] = 42

        response = self.client.get('/chatbot/99')
        self.assertEqual(response.status_code, 302)

    def test_view_chatbot_page_redirects_for_unauthenticated(self):
        response = self.client.get('/chatbot/42')
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()
