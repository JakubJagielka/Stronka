from flask import Flask, render_template, request, redirect, url_for
from optymalizacja_projekt import PostUtils
app = Flask(__name__)


# start page with first 4 posts
posts = PostUtils.getPosts().filterPosts(4, [0, 2147483646])

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # tu biore wartosc z wejscia liczby postow
        try:
            amountOfPosts = int(request.form['value'])  # retrieving value from form
        except ValueError:
            amountOfPosts = 10

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

        posts = PostUtils.getPosts().filterPosts(amountOfPosts, [lowerLimit, upperLimit])

        return render_template('index.html', posts=posts)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        new_id = len(posts) + 1
        posts.append({"id": new_id, "content": content})
        return redirect(url_for('index'))
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
