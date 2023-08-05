import os

from flask import Flask, render_template

from . import run, config
from oligodimer.core import version

app = Flask(__name__)
@app.route('/')
def index():
    check = config.check()
    if check['status'] == 'error':
        return render_template('error.html', msg=check['msg'])
    else:
        return render_template('index.html', ver=version.get())

app.register_blueprint(run.bp)

