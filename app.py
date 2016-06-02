#MAKE IT GO FFUUUUUUCCCCKKK

from flask import Flask, request
import site
dir2Add = './src'
site.addsitedir(dir2Add)
import LiquorLocator
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('osm-map-demo.html')

@app.route('/get')
def getLiquorStoreDemo():
    demoPoints = [-126.844567, 49.97859, -122.799997, 58.925305]
    rl = LiquorLocator.RouteLiquor(demoPoints)
    rl.calcInitialRoute(testpoints)
    rl.getBB()
    rl.getMeTheLiquor()
    rl.getBestRoute()    
    return jsonify(result={"status": 200})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
