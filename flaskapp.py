import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory
import site
dir2Add = './src'
site.addsitedir(dir2Add)
import LiquorLocator



app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.route('/get')
def getLiquorStoreDemo():
    demoPoints = [-126.844567, 49.97859, -122.799997, 58.925305]
    rl = LiquorLocator.RouteLiquor(demoPoints)
    rl.calcInitialRoute(testpoints)
    rl.getBB()
    rl.getMeTheLiquor()
    rl.getBestRoute()    
    return jsonify(result={"status": 200})

@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"

if __name__ == '__main__':
    app.run()