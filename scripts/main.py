import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from major.btd6_start import *

def pipeline():
    """
    Main pipeline to start BTD6 and execute additional functionality.
    """
    logging.info("Starting BTD6 pipeline...")
    btd6_start()
    # Future functionality:
    # test_functions()
    # train_model()
    # use_model()
    logging.info("Pipeline completed.")

if __name__ == "__main__":
    pipeline()
