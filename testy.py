import unittest
from locust import task, between, HttpUser
from main import app
from optymalizacja_projekt import PostUtils, CommentUtils
import requests
import cProfile
from memory_profiler import memory_usage

app = app.test_client()
app.testing = True


class FlaskAppTests(unittest.TestCase):
    """
    Testowanie porstych endpointow aplikacji, strony glownej, strony z formularzem, strony z komentarzami
    """
    def setUp(self):
        self.app = app

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_post_page(self):
        response = self.app.get('/post.html?id=1')
        self.assertEqual(response.status_code, 200)

    @staticmethod
    def test_send_request(self):
        url = 'http://127.0.0.1:5000/submit'
        some_data = {
            'value': '5',
            'Lower_Limit': '10',
            'Upper_Limit': '100'
        }

        response = requests.post(url, data=some_data)  # 'data=' sends form-encoded data
        assert response.status_code == 200



class PostUtilsTest(unittest.TestCase):
    """
    Testowanie funkcji getPosts oraz filterPosts
    """
    def test_get_posts(self):
        pl = PostUtils.getPosts()
        
        # sprawdzam czy obiekt jest typu PostList i czy lista postow jest wieksza od 0
        self.assertIsInstance(pl, PostUtils.PostList)
        self.assertGreater(len(pl.posts), 0)


    def test_filterPosts(self):
        # mockowy zbior postow, atrybuty ograniczylem do tylko tych istotnych dla filtra i testow
        # testowanie filtrów, wewnetrzne api
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
    """
    Testowanie funkcji getComments
    """
    def test_get_comments(self):
        comments = CommentUtils.getComments(1)
        # sprawdzam czy dostalem dobry typ danych wysylajac request o komentarze
        self.assertIsInstance(comments, list)


class Test_PerformanceTest(unittest.TestCase):
    """
    Testowanie wydajnosci aplikacji
    """

    wait_time = between(1,5)

    def setUp(self):
        self.client = app

    @task
    def test_home_page(self):
        self.client.get("/")

    @task(3)
    def test_comments_page(self):
        self.client.get("/post.html?id=1")

    @task
    def test_all_comment_pages(self):
        for i in range(1, 100):
            self.client.get(f"/post.html?id={i}")

    @task(2)
    def test_submit_page(self):
        data = {'value': '5', 'Lower_Limit': '10', 'Upper_Limit': '100'}
        self.client.post('/submit', json=data)
        self.client.get('/')
        data = {'value': '200', 'Lower_Limit': '1', 'Upper_Limit': '100'}
        self.client.post('/submit', json=data)
        self.client.get('/')




