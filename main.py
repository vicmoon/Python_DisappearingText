from flask import Flask, jsonify, request, render_template
import time
import threading

app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")  # Serve the frontend


@app.route("/process_input", methods=['POST'])
def process_input():
    data = request.json
    text = data.get('text', ' ')

    return jsonify({"status": "success", "message": "Received text: " + text})

    
@app.route("/delete_text", methods=['POST'])
def delete_text():
    text = ''
    return jsonify({"status": "success", "message": "Text deleted" })


if __name__ == "__main__":
    app.run(debug=True)
