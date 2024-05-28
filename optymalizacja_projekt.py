import asyncio
import httpx
import requests
import time

class PostUtils:
    class PostList:
        def __init__(self, posts: list[dict[str, any]]) -> None:
            self.posts = posts
        
        # {'userId': int, 'id': int, 'title': str, 'body': str, 'url': str}
        def filterPosts(self, amount: int,  filter: list[int]) -> list[dict[str, any]]:
            self.filteredPosts = []
            for i in self.posts:
                if len(i['title']) in range(filter[0], filter[1]):
                    self.filteredPosts.append(i)
            self.filteredPosts = self.filteredPosts[:amount]
            return self.filteredPosts

    @staticmethod
    async def getPosts() -> PostList:
        async with httpx.AsyncClient() as client:
            start = time.time()

            posts_resp = await client.get('https://jsonplaceholder.typicode.com/posts')

            photos_resp = await client.get('https://jsonplaceholder.typicode.com/photos')

            posts = posts_resp.json()

            photos = photos_resp.json()

            print(f'Posts fetched in {time.time() - start} seconds')

        bundle = PostUtils.PostList([{**posts[index], 'url': photos[index]['url']} for index in range(len(posts))])

        return bundle
    
class CommentUtils:
    @staticmethod
    async def getComments(postId: int) -> list[dict[str, any]]:
        async with httpx.AsyncClient() as client:
            start = time.time()

            comments_resp = await client.get('https://jsonplaceholder.typicode.com/comments')

            comments = comments_resp.json()

            print(f'Comments fetched in {time.time() - start} seconds')

        validComments = [comment for comment in comments if comment['postId'] == postId]

        return validComments

class ErrorUtils:
    @staticmethod
    def translateErrorToString(errorCode: int) -> str:
        if errorCode == 0:
            return ''
        errorMsg = 'Error: '
        if errorCode & 4:
            errorMsg += 'Incorrect amount of posts, '
        if errorCode & 2:
            errorMsg += 'Incorrect lower post length limit, '
        if errorCode & 1:
            errorMsg += 'Incorrect upper limit, '
        if errorCode & 8:
            errorMsg += 'No posts found that match the criteria'
        return errorMsg
