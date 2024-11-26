from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from llama_backend import Chat
from chromadb.errors import InvalidCollectionException
from Vector_database_backend import vector_data_base
import os
import PyPDF2


database = vector_data_base()
sessions = {}
user_rooms = {}

app = Flask(__name__)
socketio = SocketIO(app)

# This stores messages temporarily (could be replaced with a database)
messages = []


# API to get all chat messages
@app.route("/api/messages/<SSID>", methods=["GET"])
def get_messages(SSID):
    if not SSID in sessions:
        sessions[SSID] = Chat(SSID=SSID)
    return jsonify(sessions[SSID].messages)


@app.route("/documents/<SSID>", methods=["POST"])
def documents(SSID):
    if request.method == "POST":
        file = request.files["file"]

        _, file_extension = os.path.splitext(file.filename)

        match file_extension:
            case ".txt":
                database.vectorize_string(file.read(), SSID, file.filename)
            case ".pdf":
                string = ""
                for i in PyPDF2.PdfReader(file).pages:
                    string += i.extract_text()
                database.vectorize_string(string, SSID, file.filename)
            case _:
                raise ("Unkown filetype")


@socketio.on("connect")
def on_connect():
    user = session.get("SSID")
    if user:
        user_rooms[user] = request.sid  # Associate user with their WebSocket session ID
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
    answer = sessions[sender].send_message(data, look_up, database)

    if not sender:
        return jsonify({"error": "User not logged in"}), 400

    content = data.get("content")

    if not content:
        return jsonify({"error": "Receiver and content are required"}), 400

    # Emit message to the receiver (send to their WebSocket room)
    if sender in user_rooms:
        room = user_rooms[sender]
        emit("new_message", {"content": answer}, room=room)
    else:
        print(f"Receiver {sender} is not connected.")


# Main entry point for running the app
if __name__ == "__main__":
    socketio.run(app, debug=True)
