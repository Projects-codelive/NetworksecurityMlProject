import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
## LOG_FILe is the format to save the log i.e day month year hours minute seconds
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
# logs_path is where the logs nedd to save it will get current working directory and in that make a folder knowns as logs
# logs directory is created
os.makedirs(logs_path, exist_ok=True)
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s %(levelname)s %(message)s",
    level=logging.INFO,
)