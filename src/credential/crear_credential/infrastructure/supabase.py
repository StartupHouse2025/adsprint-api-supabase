from supabase import create_client

class SupabaseCrearCredential:
    def __init__(self, url: str, key: str) -> None:
        self.client = create_client(url, key)

    def CrearCredentialConnect(self):
        # Retorna la tabla "credential" de Supabase
        return self.client.table("credential")
