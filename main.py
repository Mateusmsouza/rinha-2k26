import argparse
import logging
import os

import numpy as np

from server_starlette import run_server
from service_search import build_ivf


def build():
    logging.critical("starting dataset build")
    import gzip
    import ijson
    import numpy as np

    file_path = "./resources/references.json.gz"

    X = []
    Y = []
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        for obj in ijson.items(f, 'item'):
            X.append(obj["vector"])
            Y.append(obj["label"])

    return np.array(X, dtype=np.float32), Y


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the app server")
    parser.add_argument("--uds", help="Unix domain socket path")
    parser.add_argument("--port", type=int, default=5000,
                        help="TCP port (ignored if --uds is set)")
    args = parser.parse_args()

    build()
    uds_path = args.uds or os.getenv("UDS_SOCKET")
    run_server(port=None if uds_path else args.port, uds=uds_path)
