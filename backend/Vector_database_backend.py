import ollama
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from chromadbx import ULIDGenerator


class vector_data_base:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="../databases",  # this doesn't do what it should, but still works????
            settings=Settings(),
            tenant=DEFAULT_TENANT,
            database=DEFAULT_DATABASE,
        )  # probably should be a persistent client but I digress
        self.SSID_vectordatabase = {}

    def vectorize_string(
        self, string: str, SSID: str, name: str, split: int = 1000, overlap: int = 250
    ) -> None:
        """sttring should be the whole document as a string, SSID for the session ID, split is the amount oof chars in a single embedding, overlap is the amount of overlap in chars inm each embedding"""
        if not SSID in self.SSID_vectordatabase:
            self.SSID_vectordatabase[SSID] = self.client.get_or_create_collection(
                name=SSID
            )
        embedding = []
        test_eqvuilant = []
        for _, j in enumerate(
            [
                string[max(i - overlap, 0) : i + split + overlap]
                for i in range(0, len(string), split)
            ]
        ):  # the monster!

            response = ollama.embeddings(
                model="mxbai-embed-large", prompt=j
            )  # should add some way to refrence the original document

            embedding.append(response["embedding"])
            test_eqvuilant.append(j)

        self.SSID_vectordatabase[SSID].add(
            ids=ULIDGenerator(len(test_eqvuilant)),
            embeddings=embedding,
            documents=test_eqvuilant,
            metadatas=[{"name": name} for _, _ in enumerate(embedding)],
        )
        # print(embedding)
        return

    def vector_retrieve(self, prompt: str, SSID: str, n_results: int = 1) -> list:
        if not SSID in self.SSID_vectordatabase:
            self.SSID_vectordatabase[SSID] = self.client.get_collection(name=SSID)
            # raise Exception("No data by that SSID")

        response = ollama.embeddings(prompt=prompt, model="mxbai-embed-large")
        results = self.SSID_vectordatabase[SSID].query(
            query_embeddings=[response["embedding"]], n_results=n_results
        )
        # print(response)
        return results

    def delete_data(self, SSID):
        try:
            self.client.delete_collection(SSID)
        except ValueError:
            print("ERROR: no data in the current session")
        if SSID in self.SSID_vectordatabase:
            self.SSID_vectordatabase.pop(SSID)


def main():
    vector_test = vector_data_base()

    vector_test.vectorize_string("this is a test too", "abc", "test2")
    vector_test.vectorize_string("qweqweqwe", "abc", "test")
    print(vector_test.vector_retrieve("qweqweqwe", "abc"))
    # print(vector_test.SSID_vectordatabase["abc"].get())


if __name__ == "__main__":
    main()
