from llama_backend import Chat
from chromadb.errors import InvalidCollectionException
from Vector_database_backend import vector_data_base
import os
import PyPDF2
import magic


def main():
    database = vector_data_base()
    session = Chat("testing")

    while True:
        help = """'E' to exit
'D' to load document
'C' to chat
'!' to delete all previous uploaded file's data
: """
        os.system("cls" if os.name == "nt" else "clear")
        match input(help):
            case "E":
                print("Exiting...")
                break
            case "D":
                try:
                    filename, file_extension = os.path.splitext(
                        input("file location : ")
                    )

                    match file_extension:
                        case ".txt":
                            with open(filename + file_extension, "r") as file:
                                database.vectorize_string(
                                    file.read(), session.SSID, input("Document name : ")
                                )
                        case ".pdf":
                            with open(filename + file_extension, "rb") as file:
                                string = ""
                                for i in PyPDF2.PdfReader(file).pages:
                                    string += i.extract_text()
                                database.vectorize_string(
                                    string, session.SSID, input("Document name : ")
                                )
                        case _:
                            raise ("Unkown filetype")
                except FileNotFoundError:
                    print("file not found")
            case "C":
                for i in session.messages:
                    match i["role"]:
                        case "system":
                            pass
                        case "user":
                            print(f"User : {i["content"]}")
                        case "assistant":
                            print(f"Assistant : {i["content"]}")

                print(
                    "print \"exit\" to exit\nstart the message with '?' for a look up"
                )
                while True:
                    user_in = input("User : ")
                    try:
                        if user_in.lower() == "exit":
                            break
                        elif user_in[0] == "?":

                            answer = session.send_message(
                                user_in[1:], look_up=True, data_base=database
                            )
                        else:
                            answer = session.send_message(user_in)
                        print(f"Assistant : {answer}")
                    except InvalidCollectionException:
                        print("No imported documents")

            case "!":
                if "y" == input("Are you sure? (N/y) : ")[0].lower():
                    database.delete_data(SSID=session.SSID)
            case _:
                print("not a command")

        input("PRESS ENTER TO CONTINUE")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
