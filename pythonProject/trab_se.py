# from flask import Flask, request, jsonify

# app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False

# @app.route('/hello')
# def say_hello():
#     return "Hello world!"
# '''
# @app.route("/", methods=["Get", "Post"])
# def form():
#     if request.method == "Post":
#         name = request.form["name"]
#         email = request.form["email"]
#         return 
        
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <title>Simple Form</title>
#         </head>
#         <body>
#             <h1>Simple Form</h1>
#             <form method="POST" action="/">
#                 <label for="name">Name:</label>
#                 <input type="text"  id="name" name="name">
#             </form>
#         </body>
#         </html>
# '''
# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/hello')
def say_hello():
    return "Hello world!"
'''
@app.route("/", methods=["Get", "Post"])
def form():
    if request.method == "Post":
        name = request.form["name"]
        email = request.form["email"]
        return 
        
        <!DOCTYPE html>
        <html>
        <head>
            <title>Simple Form</title>
        </head>
        <body>
            <h1>Simple Form</h1>
            <form method="POST" action="/">
                <label for="name">Name:</label>
                <input type="text"  id="name" name="name">
            </form>
        </body>
        </html>
'''
if __name__ == "__main__":
    app.run(debug=True, port = 5001, host="0.0.0.0")
