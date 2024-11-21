import ollama
import chromadb
from chromadbx import ULIDGenerator


class vector_data_base:
    def __init__(self):
        self.SSID_vectordatabase = {}

        self.client = (
            chromadb.Client()
        )  # probably should be a persistent client but I digress

    def vectorize_string(
        self, string: str, SSID: str, name: str, split: int = 100, overlap: int = 25
    ) -> None:
        """sttring should be the whole document as a string, SSID for the session ID, split is the amount oof chars in a single embedding, overlap is the amount of overlap in chars inm each embedding"""
        if not SSID in self.SSID_vectordatabase:
            self.SSID_vectordatabase[SSID] = self.client.create_collection(name=SSID)
        embedding = []
        test_eqvuilant = []
        for k, j in enumerate(
            [string[i - overlap : i + overlap] for i in range(0, len(string), split)]
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
            raise Exception("No data by that SSID")
        response = ollama.embeddings(prompt=prompt, model="mxbai-embed-large")
        results = self.SSID_vectordatabase[SSID].query(
            query_embeddings=[response["embedding"]], n_results=n_results
        )
        # print(response)
        return results


def main():
    vector_test = vector_data_base()

    vector_test.vectorize_string("this is a test too", "abc", "test2")
    vector_test.vectorize_string("qweqweqwe", "abc", "test")
    print(vector_test.vector_retrieve("qweqweqwe", "abc"))
    # print(vector_test.SSID_vectordatabase["abc"].get())


if __name__ == "__main__":
    main()
