"""API configuration using environment variables."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
BASE_URL = os.getenv('BASE_URL', 'https://api.example.com')
TIMEOUT = int(os.getenv('TIMEOUT', '10'))
