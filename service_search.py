import faiss
import numpy as np

INDEX = None


def load_index(file_path: str):
    # TODO call this function in main before set ready to receive api calls
    INDEX = faiss.read_index(file_path)


def search(x: np.ndarray):
    k = 5
    distances, indices = INDEX.search(x, k)
