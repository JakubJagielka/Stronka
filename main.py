from flask import Flask, render_template, request
from optymalizacja_projekt import PostUtils, CommentUtils
app = Flask(__name__)


# Początkowe 4 posty na stronie
posts = PostUtils.getPosts().filterPosts(4, [0, 2147483646])

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # tu prubuje wziąść wartosc z wejscia liczby postow
        try:
            amountOfPosts = int(request.form['value'])  # zdobycie wartosci z formularza
        except ValueError:
            amountOfPosts = 10 #bazowa wartosc

        # tu zbieram wartosci z 2 pol dolnego i gornego limitu dlugosci postu
        try:
            lowerLimit = int(request.form['Lower_Limit'])
        except:
            lowerLimit = 0
        try:
            upperLimit = int(request.form['Upper_Limit'])
        except ValueError:
            upperLimit = 2147483646

        if upperLimit <= lowerLimit:
            upperLimit = lowerLimit +1

        global posts
        posts = PostUtils.getPosts().filterPosts(amountOfPosts, [lowerLimit, upperLimit])

        return render_template('index.html', posts=posts)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', posts=posts)

@app.route('/post.html')
def post():
    # Zdobycie id z adresu url aby wiedzieć, który post wyświetlić
    try:
        post_id = request.args.get('id')
        # Znalezienie postu o danym id
    except:
        return "Something went wrong", 404
    post = next((p for p in posts if str(p['id']) == post_id), None)
    comments = CommentUtils.getComments(int(post_id))
    if post:
        return render_template('post.html', post=post, comments=comments)
    else:
        return "Post not found", 404

if __name__ == '__main__':
    app.run(debug=True)
