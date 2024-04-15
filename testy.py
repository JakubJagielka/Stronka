import unittest
from unittest.mock import patch, Mock
from main import app
from optymalizacja_projekt import PostUtils, CommentUtils

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
    def test_get_posts(self):
        pl = PostUtils.getPosts()

        # sprawdzam czy obiekt jest typu PostList i czy lista postow jest wieksza od 0
        self.assertIsInstance(pl, PostUtils.PostList)
        self.assertGreater(len(pl.posts), 0)
    
    def test_filterPosts(self):
        # mockowy zbior postow, atrybuty ograniczylem do tylko tych istotnych dla filtra i testow
        mock_posts = [
            {"id": 1, "user_id": 11, 'title': '1'},
            {"id": 2, "user_id": 12, 'title': '12'},
            {"id": 3, "user_id": 11, 'title': '123'},
            {"id": 4, "user_id": 13, 'title': '12345'},
            {"id": 5, "user_id": 15, 'title': '1234'},
        ]

        # Wywołanie metody filterPosts
        post_list = PostUtils.PostList(mock_posts)
        filtered_posts = post_list.filterPosts(5, [2, 5])

        # sprawdzam czy sa tylko 3 wyniki bo tyle przepuszcza powyzszy filtr
        self.assertEqual(len(filtered_posts), 3)
        
        # sprawdzam po kolei id postow zeby zobaczyc czy filtr przepuscil te spelniajace jego warunki
        self.assertEqual(filtered_posts[0]["id"], 2)
        self.assertEqual(filtered_posts[1]["id"], 3)
        self.assertEqual(filtered_posts[2]["id"], 5)


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