from flask import Flask
from cyclrr import create_app

app = Flask(__name__, static_url_path='')
app = create_app(app)
print(app.url_map)

if __name__ == '__main__':
    app.run()
