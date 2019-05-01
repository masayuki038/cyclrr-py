from flask import Flask, render_template
from cyclrr import setup

app = Flask(__name__, static_url_path='', template_folder='static')
app = setup(app)

@app.route("/")
def index():
    return render_template('index.html')

print(app.url_map)

if __name__ == '__main__':
    app.run()
