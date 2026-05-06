import numpy as np

from service_vector import vectorize_transaction

# build phase


def build_dataset(raw_data: list[dict]):
    X = np.array([vectorize_transaction(x)
                 for x in raw_data], dtype=np.float32)
    return np.ascontiguousarray(X)


def kmeans(X, k, n_iter=20):
    n, d = X.shape
    centroids = X[np.random.choice(n, k, replace=False)]

    for _ in range(n_iter):
        distances = ((X[:, None, :] - centroids[None, :, :])**2).sum(axis=2)
        labels = distances.argmin(axis=1)

        for i in range(k):
            points = X[labels == i]
            if len(points) > 0:
                centroids[i] = points.mean(axis=0)

    return centroids, labels


def build_ivf(X, nlist):
    centroids, labels = kmeans(X, nlist)

    lists = [[] for _ in range(nlist)]
    for idx, label in enumerate(labels):
        lists[label].append(idx)

    lists = [np.array(lst, dtype=np.int32) for lst in lists]

    return centroids, lists

# hot path


def search_ivf_vec(query, X, centroids, lists, nprobe=3, k=5):
    d_centroids = np.sum((centroids - query)**2, axis=1)
    probe_ids = np.argpartition(d_centroids, nprobe)[:nprobe]

    candidate_ids = np.concatenate([lists[i] for i in probe_ids])
    if candidate_ids.size == 0:
        return np.array([], dtype=np.int32)

    candidates = X[candidate_ids]

    dists = np.sum((candidates - query)**2, axis=1)

    topk = np.argpartition(dists, k)[:k]

    return candidate_ids[topk]


if __name__ == "__main__":
    import json
    import gzip
    file_path = "./resources/references.json.gz"
    with gzip.open(file_path, 'rt', encoding='UTF-8') as zip_file:
        data = json.load(zip_file)
        X = []
        Y = []
        for instance in data:
            X.append(instance["vector"])
            Y.append(instance["label"])
        X = np.array(X, dtype=np.float32)
        centroids, lists = build_ivf(X, nlist=30)
        print(X.shape)
