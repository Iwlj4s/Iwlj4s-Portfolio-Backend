import os
from dotenv import load_dotenv

from pathlib import Path

env_path = Path('.') / '.env'  # Getting env path
load_dotenv(dotenv_path=env_path)  # Load env


class Settings:
    """
    Get important data from env file
    """
    DATABASE_URL: str = os.getenv('DB_LITE')
    DATABASE_URL_FOR_ALEMBIC: str = os.getenv('DB_FOR_ALEMBIC')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = os.getenv('ALGORITHM')
    GITHUB_CLIENT_ID: str = os.getenv('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET: str = os.getenv('GITHUB_CLIENT_SECRET')
    GITHUB_AUTH_URL: str = os.getenv('GITHUB_AUTH_URL')
    GITHUB_TOKEN_URL: str = os.getenv('GITHUB_TOKEN_URL')
    GITHUB_USER_URL: str = os.getenv('GITHUB_USER_URL')
    ALLOWED_GITHUB_ID: str = os.getenv('ALLOWED_GITHUB_ID')


settings = Settings()  # Create object for easy import and use them


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}
