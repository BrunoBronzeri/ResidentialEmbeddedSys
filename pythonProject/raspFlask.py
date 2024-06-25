from flask import Flask, render_template, redirect, request, url_for, Response

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/hello')
def say_hello():
    return "Hello world, carai!"

if __name__ == "__main__":
    app.run(debug=True, port = 5001, host="0.0.0.0")
