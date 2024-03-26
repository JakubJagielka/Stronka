import unittest
from unittest.mock import patch
from main import app, PostUtils, CommentUtils

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        # Testowanie strony głównej
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_submit_post(self):
        # Testowanie strony z formularzem
        response = self.app.post('/submit', data={'value': '5', 'Lower_Limit': '10', 'Upper_Limit': '100'})
        self.assertEqual(response.status_code, 200)

        # Testowanie storny z komentarzami
    def test_post_page(self):
        # Directly appending query parameters to the URL
        response = self.app.get('/post.html?id=1')
        self.assertEqual(response.status_code, 200)


class PostUtilsTest(unittest.TestCase):
    # Testowanie funkcji getPosts
    @patch('requests.get')
    def test_get_posts(self, mock_requests_get):
        mock_requests_get.return_value.json.return_value = [
            {'userId': 1, 'id': 1, 'title': 'Test Title', 'body': 'Test body', 'url': 'Test URL'}
        ]

        posts = PostUtils.getPosts()
        self.assertIsInstance(posts, PostUtils.PostList)
        self.assertEqual(len(posts.posts), 1)


class CommentUtilsTest(unittest.TestCase):
    # Testowanie funkcji getComments
    @patch('requests.get')
    def test_get_comments(self, mock_requests_get):
        mock_requests_get.return_value.json.return_value = [
            {'postId': 1, 'id': 1, 'name': 'Test Comment', 'email': 'test@example.com', 'body': 'Test Body'}
        ]

        comments = CommentUtils.getComments(1)
        self.assertIsInstance(comments, list)
        self.assertEqual(len(comments), 1)


if __name__ == '__main__':
    unittest.main()