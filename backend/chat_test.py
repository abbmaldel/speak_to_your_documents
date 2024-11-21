from llama_backend import Chat
from Vector_database_backend import vector_data_base
import os


def main():
    database = vector_data_base()
    session = Chat("testing")

    while True:
        help = """'E' to exit
'D' to load document
'C' to chat
: """
        os.system("cls" if os.name == "nt" else "clear")
        match input(help):
            case "E":
                print("Exiting...")
                break
            case "D":
                try:
                    with open(input("file location : ")) as file:
                        database.vectorize_string(
                            file.read(), session.SSID, input("Document name : ")
                        )
                except FileNotFoundError:
                    print("file not found")
            case "C":
                print(
                    "print \"exit\" to exit\nstart the message with '?' for a look up"
                )
                while True:
                    user_in = input("User : ")
                    if user_in.lower() == "exit":
                        break
                    elif user_in[0] == "?":
                        answer = session.send_message(
                            user_in[1:], look_up=True, data_base=database
                        )
                    else:
                        answer = session.send_message(user_in)
                    print(f"Assistant : {answer}")
        input("PRESS ENTER TO CONTINUE")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
