from credential.crear_credential.infrastructure.supabase import SupabaseCrearCredential
from ..application.response import CrearCredentialResponse

class CrearCredentialController:

    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase_credential = SupabaseCrearCredential(supabase_url, supabase_key)
        self.response = CrearCredentialResponse()

    def crear_credential(self, data):
        table = self.supabase_credential.CrearCredentialConnect()
        status = self.response.SetCrearCredential(table, data)
        return status


