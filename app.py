from flask import Flask
app = Flask(__name__)
import LiquorLocator

@app.route("/")
def hello():
    return "Hello World!"

def getLiquorStoreDemo():
    demoPoints = [-126.844567, 49.97859, -122.799997, 58.925305]
    LiquorLocator.RouteLiquor(demoPoints)
    rl.calcInitialRoute(testpoints)
    rl.getBB()
    rl.getMeTheLiquor()
    rl.getBestRoute()

    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)