import pytest
import httpx
from multiprocessing import Process
from main import app
from optymalizacja_projekt import PostUtils, CommentUtils

# Helper function to run the Flask app

def run_app():

    app.run(port=5000)


@pytest.fixture(scope="module", autouse=True)
def start_flask_app():
    proc = Process(target=run_app)
    proc.start()
    yield proc.terminate()
    proc.join()

class TestFlaskApp:
    """
    Testowanie porstych endpointow aplikacji, strony glownej, strony z formularzem, strony z komentarzami
    """
    @pytest.mark.asyncio
    async def test_index_page(self):
        async with httpx.AsyncClient(base_url="http://127.0.0.1:5000") as client:
            response = await client.get('/')
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_post_page(self):
        async with httpx.AsyncClient(base_url="http://127.0.0.1:5000") as client:
            response = await client.get('/post.html?id=1')
            assert response.status_code == 200


    @pytest.mark.asyncio
    async def test_send_request(self):
        url = 'http://127.0.0.1:5000/submit'
        some_data = {
            'value': '5',
            'Lower_Limit': '10',
            'Upper_Limit': '100'
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=some_data)
            assert response.status_code == 200

class TestPostUtils:
    """
    Testowanie funkcji getPosts oraz filterPosts
    """
    @pytest.mark.asyncio
    async def test_get_posts(self):
        pl = await PostUtils.getPosts()
        # sprawdzam czy obiekt jest typu PostList i czy lista postow jest wieksza od 0
        assert isinstance(pl, PostUtils.PostList)
        assert len(pl.posts) > 0


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
        assert len(filtered_posts) == 3

        # sprawdzam po kolei id postow zeby zobaczyc czy filtr przepuscil te spelniajace jego warunki
        assert filtered_posts[0]["id"] == 2
        assert filtered_posts[1]["id"] == 3
        assert filtered_posts[2]["id"] == 5


class TestCommentUtils:
    """
    Testowanie funkcji getComments
    """
    @pytest.mark.asyncio
    async def test_get_comments(self):
        comments = await CommentUtils.getComments(1)
        # sprawdzam czy dostalem dobry typ danych wysylajac request o komentarze
        assert isinstance(comments, list)


class TestPerformance:
    """
    Testowanie wydajnosci aplikacji
    """
    @pytest.mark.asyncio
    async def test_performance(self):
        async with httpx.AsyncClient(base_url="http://127.0.0.1:5000") as client:
            await client.get("/")
            await client.get("/post.html?id=1")
            for i in range(1, 100):
                await client.get(f"/post.html?id={i}")
            data = {'value': '5', 'Lower_Limit': '10', 'Upper_Limit': '100'}
            await client.post('/submit', json=data)
            await client.get('/')
            data = {'value': '200', 'Lower_Limit': '1', 'Upper_Limit': '100'}
            await client.post('/submit', json=data)
            await client.get('/')