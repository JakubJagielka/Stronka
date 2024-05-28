from flask import Flask, render_template, request
from optymalizacja_projekt import PostUtils, CommentUtils, ErrorUtils
import cProfile
import asyncio

app = Flask(__name__)

# Początkowe 4 posty na stronie
posts = asyncio.run(PostUtils.getPosts()).filterPosts(100, [0, 2147483646])

@app.route('/submit', methods=['POST'])
async def submit():
    errorCode = 0
    if request.method == 'POST':
        # tu prubuje wziąść wartosc z wejscia liczby postow
        amountOfPosts = request.form['value']
        if amountOfPosts == '':
            amountOfPosts = 100
        try:
            amountOfPosts = int(amountOfPosts)  # zdobycie wartosci z formularza
        except ValueError:
            amountOfPosts = 100  # bazowa wartosc
            errorCode |= 4

        # tu zbieram wartosci z 2 pol dolnego i gornego limitu dlugosci postu
        lowerLimit = request.form['Lower_Limit']
        if lowerLimit == '':
            lowerLimit = 0
        try:
            lowerLimit = int(lowerLimit)
        except:
            lowerLimit = 0
            errorCode |= 2

        upperLimit = request.form['Upper_Limit']
        if upperLimit == '':
            upperLimit = 2147483646
        try:
            upperLimit = int(upperLimit)
        except ValueError:
            upperLimit = 2147483646
            errorCode |= 1

        if upperLimit <= lowerLimit:
            upperLimit = lowerLimit + 1

        global posts
        posts = await PostUtils.getPosts()
        posts = posts.filterPosts(amountOfPosts, [lowerLimit, upperLimit])

        if len(posts) == 0:
            errorCode |= 8
        errorCode = ErrorUtils.translateErrorToString(errorCode)
        return render_template('index.html', posts=posts, errorCode=errorCode)


@app.route('/', methods=['GET', 'POST'])
async def index():
    return render_template('index.html', posts=posts)


@app.route('/post.html')
async def post():
    # Zdobycie id z adresu url aby wiedzieć, który post wyświetlić
    try:
        post_id = request.args.get('id')
        # Znalezienie postu o danym id
    except:
        return "Something went wrong", 404
    post = next((p for p in posts if str(p['id']) == post_id), None)
    comments = await CommentUtils.getComments(int(post_id))
    if post:
        return  render_template('post.html', post=post, comments=comments)
    else:
        return "Post not found", 404


if __name__ == '__main__':

    app.run(debug=True)
