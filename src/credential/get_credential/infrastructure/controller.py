from src.credential.get_credential.infrastructure.supabase import SupabaseCredential
from ..application.response import CredentialResponse

class CredentialController:

    def __init__(self):
        self.supabase_credential = SupabaseCredential()
        self.response = CredentialResponse()

    def authenticate_credential(self, credential, pasw):
        credential_info = self.supabase_credential.CredentialConnect(credential, pasw)
        parsed = self.response.parsedCredential(credential_info)
        return parsed


