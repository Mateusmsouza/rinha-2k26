import logging
import os

from service_pre_process_dataset import preprocess_dataset


def build():
    logging.info("Starting dataset build...")
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_PATH = os.path.join(CURRENT_DIR, "resources")
    file_path = os.getenv("DATASET_PATH", os.path.join(BASE_PATH, "references.json.gz"))
    
    if not os.path.exists(file_path):
        logging.error(f"Dataset file not found at {file_path}")
        return

    index = preprocess_dataset(file_path)

    if index is None:
        raise RuntimeError("Dataset build failed during preprocessing")

    logging.info("Dataset build completed successfully")

if __name__ == "__main__":
    build()