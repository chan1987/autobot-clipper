from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/my-link/')
def my_link():
    print('I got clicked!')

    return 'Click.'


@app.route('/script/')
def run_script():
    file = open(r'/autobot-clipper/ytbot.py', 'r').read()
    return exec(file)


@app.route('/addRegion', methods=['POST'])
def addRegion():
    ...
    return request.form['projectFilePath']


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
