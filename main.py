from flask import Flask, render_template, request, redirect, url_for
from optymalizacja_projekt import PostUtils
app = Flask(__name__)

# Simulate a posts database with a list
'''posts = [
    {"id": 1, "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.","url":"https://preview.redd.it/a-rare-hybrid-of-nord-and-imga-v0-o4ovn3il8nba1.png?width=640&crop=smart&auto=webp&s=ddc3c8006041bf1f290b21a679670cf0dfa862fb"},
    {"id": 2, "content": "Pellentesque vitae velit ex.","url":"https://preview.redd.it/a-rare-hybrid-of-nord-and-imga-v0-o4ovn3il8nba1.png?width=640&crop=smart&auto=webp&s=ddc3c8006041bf1f290b21a679670cf0dfa862fb"},
    {"id": 3, "content": "Mauris dapibus risus quis suscipit vulputate.","url":"https://preview.redd.it/a-rare-hybrid-of-nord-and-imga-v0-o4ovn3il8nba1.png?width=640&crop=smart&auto=webp&s=ddc3c8006041bf1f290b21a679670cf0dfa862fb"},
    {"id": 4, "content": "Mauris dadadadpibus risus quis suscipit vulputate.","url":"https://preview.redd.it/a-rare-hybrid-of-nord-and-imga-v0-o4ovn3il8nba1.png?width=640&crop=smart&auto=webp&s=ddc3c8006041bf1f290b21a679670cf0dfa862fb"}
]'''
posts = PostUtils.getPosts().filterPosts(4, [0, 2147483646])

@app.route('/submit', methods=['POST'])
def submit():
    # jesli n to
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
