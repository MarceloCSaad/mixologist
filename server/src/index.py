from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/ping", methods=["GET"])
def get_ping():
    return jsonify({"message": "pong"})


@app.post("/drink")
def post_drink():
    return jsonify({"message": "drink"})


if __name__ == "__main__":
    app.run(debug=True)
