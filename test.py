Type "help", "copyright", "credits" or "license()" for more information.
>>> from flask import Flask
... 
... app = Flask(__name__)
... 
... @app.route('/')
... def home():
...     return 'Hello, Flask!'
... 
... if __name__ == '__main__':
...     app.run(debug=True)
