from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulate a posts database with a list
posts = [
    {"id": 1, "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
    {"id": 2, "content": "Pellentesque vitae velit ex."},
    {"id": 3, "content": "Mauris dapibus risus quis suscipit vulputate."},
    {"id": 4, "content": "Mauris dadadadpibus risus quis suscipit vulputate."}
]

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        value = request.form['value']  # retrieving value from form
        length = len(value)
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