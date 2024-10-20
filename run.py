# Archivo: run.py

import os
from app import create_app
from dotenv import load_dotenv

load_dotenv(override=True)


app = create_app()

if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG', True))
