from flask import Flask, request, jsonify, render_template
import threading
from main import command_listener, greet_user  # your existing assistant code

app = Flask(__name__)
from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('index.html')  # your HTML in same folder



@app.route('/speak', methods=['POST'])
def speak_command():
    data = request.get_json()
    command = data.get('command', '')
    if command:
        threading.Thread(target=command_listener, args=(command,)).start()
        return jsonify({"status": "success", "message": f"Processing command: {command}"})
    return jsonify({"status": "error", "message": "No command received."})

@app.route('/greet', methods=['GET'])
def greet():
    threading.Thread(target=greet_user).start()
    return jsonify({"message": "Greeting sent!"})

if __name__ == "__main__":
    app.run(debug=True)
