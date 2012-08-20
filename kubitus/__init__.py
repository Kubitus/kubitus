from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html.jinja2')

@app.route('/<string:page>/')
def page(page):
    return render_template('%s.html.jinja2' % page)
