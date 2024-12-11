from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
import PyPDF2
from uuid import uuid4


sessions = {}
user_rooms = {}

app = Flask(__name__)
CORS(app, origins="*")
socketio = SocketIO(app, cors_allowed_origins="*", cookie={"name": "sid"})

# This stores messages temporarily (could be replaced with a database)
messages = []


# API to get all chat messages
@app.route("/api/messages/<SSID>", methods=["GET"])
def get_messages(SSID):

    return jsonify(
        [
            {"role": "system", "content": "system_message"},
            {"role": "user", "content": "Test string"},
        ].messages
    )


@app.route("/documents/<SSID>", methods=["POST"])
def documents(SSID):
    print("SSID from request", SSID)
    if request.method == "POST":
        file = request.files["file"]
        _, file_extension = os.path.splitext(file.filename)
        match file_extension:
            case ".txt":
                pass
                return jsonify({"message": "success"}), 200
            case ".pdf":
                pass
                return jsonify({"message": "success"}), 200
            case _:
                return jsonify({"message": "error"}), 400
                raise ("Unkown filetype")
        return jsonify({"message": "success"}), 200


@socketio.on("connect")
def on_connect(socket):
    session["SSID"] = str(request.sid)
    user = session.get("SSID")
    print(session)
    if user:
        print("Request", request.sid)
        user_rooms[user] = request.sid  # Associate user with their WebSocket session ID
        emit("cookie", {"SSID": user})
        join_room(user)
        print(f"{user} connected.")


# WebSocket Event to Handle Disconnect
@socketio.on("disconnect")
def on_disconnect():
    user = session.get("SSID")
    if user and user in user_rooms:
        leave_room(user)
        del user_rooms[user]
        print(f"{user} disconnected.")


@socketio.on("send_message")
def handle_send_message(data, look_up):
    sender = session.get("SSID")
    if not sender:
        return jsonify({"error": "User not logged in"}), 400
    answer = "just a test answer"
    # content = data.get("content")

    # if not content:
    #    return jsonify({"error": "Receiver and content are required"}), 400

    # Emit message to the receiver (send to their WebSocket room)
    if sender in user_rooms:
        room = user_rooms[sender]
        emit("new_message", {"content": answer}, room=room)
    else:
        print(f"Receiver {sender} is not connected.")


# Main entry point for running the app
if __name__ == "__main__":
    socketio.run(app, debug=True)
