import os
from app import create_app
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


app = create_app()


if __name__ == '__main__':
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    app.run(host=HOST, port=PORT, debug=DEBUG)
