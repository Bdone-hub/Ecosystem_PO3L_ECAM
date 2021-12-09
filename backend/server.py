import json
import os
import time

import flask
import testBackend

root = os.path.join(
    os.path.dirname(os.path.abspath(__file__)).removesuffix("/backend"), "frontend"
)

examples = os.path.join(
    os.path.dirname(os.path.abspath(__file__)).removesuffix("/backend"),
    "ecosystemExampleFiles",
)


app = flask.Flask(__name__)


# Ping the API
@app.route("/pingAPI", methods=["GET"])
def pingAPI():
    return testBackend.testBackendCall()


# Main API
# For now it only responds with a modification of a JSON object it received
@app.route("/API", methods=["POST"])
def api():
    data = flask.request.form.getlist("json")
    jsonFile = json.loads(data[0])
    print(jsonFile)
    jsonFile["response"] = "Answer from the backend :D"
    time.sleep(10)
    return jsonFile


@app.route("/API/load", methods=["GET"])
def loadExample():
    file = open(os.path.join(examples, "example1.json"), "r+").read()
    return file


# Homepage
@app.route("/", methods=["GET"])
def index():
    return flask.send_from_directory(root, "index/index.html")


# Simulate
@app.route("/simulate", methods=["GET"])
def simulate():
    return flask.send_from_directory(root, "simulate/index.html")


# About
@app.route("/about", methods=["GET"])
def about():
    return "beep boop I'm a flask server running on a proxmox VM in a basement somewhere in Belgium"
    # flask.send_from_directory(root, "about/index.html")


# Ping the website (used for GitHub Badge)
@app.route("/ping", methods=["GET"])
def ping():
    return "Website is up ⛄️"


# Route for js, css, images, ...
@app.route("/<path:path>", methods=["GET"])
def static_proxy(path):
    return flask.send_from_directory(root, path)


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")
