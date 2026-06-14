import os


class Config:
    BASE_DIR = os.path.dirname(__file__)

    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'parkinsons.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MODEL_PATH = os.getenv(
        "MODEL_PATH", os.path.join(BASE_DIR, "trained_models", "best_model.pkl")
    )
    MODEL_METADATA_PATH = os.getenv(
        "MODEL_METADATA_PATH",
        os.path.join(BASE_DIR, "trained_models", "model_metadata.json"),
    )
    FEATURE_NAMES_PATH = os.getenv(
        "FEATURE_NAMES_PATH",
        os.path.join(BASE_DIR, "trained_models", "feature_names.json"),
    )
    DATASET_PATH = os.getenv(
        "DATASET_PATH", os.path.join(BASE_DIR, "dataset", "original_dataset.csv")
    )

    LOG_DIR = os.getenv("LOG_DIR", os.path.join(BASE_DIR, "logs"))
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    RATE_LIMIT = os.getenv("RATE_LIMIT", "100 per hour")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    PORT = int(os.getenv("PORT", "5000"))
