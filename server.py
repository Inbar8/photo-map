from flask import Flask, send_file, jsonify
import random
import photo_map

app = Flask(__name__)

@app.get("/data.json")
def data():
    # Do all of the photomap stuff
    return jsonify(photo_map.get_all_locations())

@app.get("/")
def index():
    return send_file("web/index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
