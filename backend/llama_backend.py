import ollama
from Vector_database_backend import vector_data_base


class Chat:
    def __init__(
        self,
        SSID,
        model: str = "llama3.2",
        options: dict = {},
        system_message: str = "You're jobb is to take out information from the given documents",
    ) -> None:
        self.messages = [{"role": "system", "content": system_message}]
        self.model = model
        self.options = options
        self.SSID = SSID

    def send_message(
        self, message: str, look_up: bool = False, data_base: vector_data_base = None
    ) -> str:
        if look_up:
            self.messages.append(
                {
                    "role": "system",
                    "content": "use the following information to respond: "
                    + data_base.vector_retrieve(message, self.SSID)["documents"][0][0],
                }
            )
        self.messages.append({"role": "user", "content": message})
        ollama_response = ollama.chat(model=self.model, messages=self.messages)
        self.messages.append(
            {"role": "assistant", "content": ollama_response["message"]["content"]}
        )
        return ollama_response["message"]["content"]


def main():
    some_chat = Chat("test")
    print(some_chat.send_message("ping"))
    print(some_chat.send_message("what did I say in my last message?"))


if __name__ == "__main__":
    main()
