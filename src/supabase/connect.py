import os
from supabase import create_client
from dotenv import load_dotenv

class SupabaseConnection:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env
        url = os.getenv("SUPABASE_URL")  # Corrected environment variable key
        key = os.getenv("SUPABASE_KEY")  # Corrected environment variable key
        self.client = create_client(supabase_url=url, supabase_key=key)

    def get_client(self):
        return self.client