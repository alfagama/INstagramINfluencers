from flask import Flask  # Flask -> class name
from flask import render_template
from flask import jsonify
import os
from web_app.funcs.db import Db

# declare application. initialize with Flask instance/class
app = Flask(__name__, template_folder='templates')

# get MongoDB instance
db = Db()


# declare route # can also declare methods to accept. like -> 'GET'
# @app.route("/", methods=['GET'])
@app.route("/")
def home():
    todos = db.find_all('todos')
    return render_template('home.html', todos=list(todos))


@app.route("/todo/<importance_val>")
def get_todo(importance_val):
    todos = db.find('todos', {"importance": int(importance_val)})
    return jsonify(todos)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5110)
