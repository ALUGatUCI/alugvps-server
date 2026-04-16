import dotenv
import os

dotenv.load_dotenv()

def read_config_file(key: str):
    return os.getenv(key)