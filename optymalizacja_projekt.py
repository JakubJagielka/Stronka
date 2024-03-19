import requests


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
    def getPosts() -> PostList:
        posts = requests.get('https://jsonplaceholder.typicode.com/posts').json()
        photos = requests.get('https://jsonplaceholder.typicode.com/photos').json()
        bundle = PostUtils.PostList([{**posts[index], 'url': photos[index]['url']} for index in range(len(posts))])
        return bundle
    
class CommentUtils:
    def getComments(postId: int) -> list[dict[str, any]]:
        comments = requests.get('https://jsonplaceholder.typicode.com/comments').json()
        i, maxI, isIdFound = 0, len(comments), False # todo optymaln petla
        validComments = []
        while i < maxI:
            # print(type(comments[i]['postId']),type( postId), comments[i]['postId'] == postId)
            if comments[i]['postId'] == postId:
                # print(1)
                validComments.append(comments[i])
            i += 1
        print(validComments)
        return validComments

def main():
    x = PostUtils.getPosts()
    print(x.posts[0])

if __name__ == '__main__':
    main()
