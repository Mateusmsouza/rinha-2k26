import argparse
import os

from server_starlette import run_server

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the app server")
    parser.add_argument("--uds", help="Unix domain socket path")
    parser.add_argument("--port", type=int, default=5000,
                        help="TCP port (ignored if --uds is set)")
    args = parser.parse_args()
    
    uds_path = args.uds or os.getenv("UDS_SOCKET")
    run_server(port=None if uds_path else args.port, uds=uds_path)
