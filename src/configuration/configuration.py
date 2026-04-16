import dotenv
import os

dotenv.load_dotenv()

def verify_config():
    # Verify that all required environment variables are set
    required_keys = [
        "secret_key", # Use this command to generate a secret key: openssl rand -hex 32
        "port",
        "acc_limit",
        "cpu_limit",
        "ram_limit",
        "disk_limit",
        "fingerprint_image",
        "email",
        "email_key",
        "smtp_host",
        "smtp_port",
    ]

    for key in required_keys:
        if not os.getenv(key):
            raise ValueError(f"Missing required configuration key: {key}")

def read_config_file(key: str):
    return os.getenv(key)