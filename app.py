from flask import Flask, url_for

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
@app.route('/test')
def test_url_for():
    print(url_for("hello"))
    print(url_for("user_page", name='a'))
    print(url_for("user_page", name='b'))
    print(url_for("test_url_for", num=2))
    return 'test page'

if __name__ == '__main__':
    app.run()
