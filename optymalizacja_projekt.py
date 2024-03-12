import requests, json


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
    def getPosts(amount: int) -> dict:
        posts = requests.get('https://jsonplaceholder.typicode.com/posts').json()
        photos = requests.get('https://jsonplaceholder.typicode.com/photos').json()
        nPosts, nPhotos = posts[:amount], photos[:amount]
        bundle = [{'postData': nPosts[index], 'photoData': nPhotos[index]} for index in range(len(nPosts))]
        return bundle
    

def main():
    x = Viewer.getPosts(4)
    print(x)

if __name__ == '__main__':
    main()
