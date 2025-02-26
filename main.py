from flask import Flask, jsonify, request, render_template
import time
import threading

app = Flask(__name__)

stored_text = ""  # Global variable to store text
last_typing_time = None  # Track last time user typed
lock = threading.Lock()  # Thread safety

def monitor_text_expiry():
    """Background thread to delete text after 5 seconds of inactivity."""
    global stored_text, last_typing_time
    while True:
        time.sleep(1)  # Check every second
        with lock:
            if last_typing_time and time.time() - last_typing_time > 10:
                stored_text = ""  # Clear stored text
                last_typing_time = None
                print("Text deleted after inactivity.")

# Start the monitoring thread
threading.Thread(target=monitor_text_expiry, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")  # Serve the frontend

@app.route("/save-text", methods=["POST"])
def save_text():
    """Save user input and reset the inactivity timer."""
    global stored_text, last_typing_time
    data = request.json
    with lock:
        stored_text = data.get("text", "")
        last_typing_time = time.time()  # Update last typing time
    return jsonify({"message": "Text saved"}), 200

@app.route("/get-text", methods=["GET"])
def get_text():
    """Retrieve the stored text."""
    return jsonify({"text": stored_text}), 200

if __name__ == "__main__":
    app.run(debug=True)
