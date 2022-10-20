from flask import Flask


app = Flask(__name__)


@app.route('/hello-world')
def hello_world():
    return 'Hello, World!'


def main():
    app.run()


if __name__ == '__main__':
    main()
