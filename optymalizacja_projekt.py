import requests


'''
CONTENT
/posts 	    100 posts
/comments 	500 comments
/albums 	100 albums
/photos 	5000 photos
/todos 	    200 todos
/users 	    10 users'''

'''response = requests.get('https://jsonplaceholder.typicode.com/posts')
print(response.json())'''
# ile postow -> n postow i n zdjec

class PostUtils:
    class PostList:
        def __init__(self, posts: list[dict[str, any]]) -> None:
            self.posts = posts
        
        '''{'userId': 1,
            'id': 1,
            'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit',
            'body': 'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto',
            'url': 'https://via.placeholder.com/600/92c952'}'''
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
    

def main():
    x = PostUtils.getPosts(4)
    print(x[0])

if __name__ == '__main__':
    main()
