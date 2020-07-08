
# $env:FLASK_APP = "server.py"
# $env:FLASK_ENV = "development"
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    lines = []
    with  open('q1.txt', 'r') as f:
        for line in f:
            lines.append(line.strip())
        
    return render_template('index.html', types=lines)