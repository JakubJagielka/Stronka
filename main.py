from flask import Flask, render_template, request, jsonify
import os

path = os.getcwd()
app = Flask(__name__)
print(path)
# Simulating a database of posts with a simple list of dictionaries
posts = [
    {"id": 1, "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
    {"id": 2, "content": "Pellentesque vitae velit ex."},
    {"id": 3, "content": "Mauris dapibus risus quis suscipit vulputate."}
]


@app.route('/')
def index():
    return render_template('index.html', posts=posts)


@app.route('/add_post', methods=['POST'])
def add_post():
    content = request.form.get('content')
    if content:
        new_id = len(posts) + 1
        posts.append({"id": new_id, "content": content})
        return jsonify({"id": new_id, "content": content})
    return 'Error', 400


@app.route('/get_posts')
def get_posts():
    return jsonify(posts)


if __name__ == '__main__':
    app.run(debug=True)

