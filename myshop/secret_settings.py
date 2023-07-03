from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    DEBUG: bool
    ALLOWED_HOSTS: str
    ENGINE: str
    NAME_DB: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: str
    EMAIL: str
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str
    EMAIL_PORT: str
    EMAIL_USE_TLS: bool
    # SOCIAL_AUTH_FACEBOOK_KEY: str
    # SOCIAL_AUTH_FACEBOOK_SECRET: str
    # SOCIAL_AUTH_GOOGLE_OAUTH2_KEY: str
    # SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET: str

    # CELERY_BROKER_URL: str
    # CELERY_RESULT_BACKEND: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
