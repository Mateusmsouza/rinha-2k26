import argparse
import logging
import os
import sys

# Adiciona o diretório atual ao caminho de busca do Python
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from core.server_starlette import run_server

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    parser = argparse.ArgumentParser(description="Start the app server")
    parser.add_argument("--uds", help="Unix domain socket path")
    parser.add_argument("--port", type=int, default=5000,
                        help="TCP port (ignored if --uds is set)")
    args = parser.parse_args()

    uds_path = args.uds or os.getenv("UDS_SOCKET")
    run_server(port=None if uds_path else args.port, uds=uds_path)
