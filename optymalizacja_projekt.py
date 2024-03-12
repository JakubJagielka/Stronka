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

class Viewer:
    @staticmethod
    def getPosts(amount: int) -> list:
        posts = list(requests.get('https://jsonplaceholder.typicode.com/posts'))
        print(len(posts[:2]))
        return posts[:amount]



def main():
    print(Viewer.getPosts(13))

if __name__ == '__main__':
    main()
