from bcrypt import checkpw
from flask import abort
from src.supabase.connect import SupabaseConnection  # Import the connection class

class SupabaseCredential:
    def __init__(self):
        # Initialize the Supabase connection
        self.client = SupabaseConnection().get_client()

    def CredentialConnect(self, credential, pasw):
        # Verificar si creditial es un email o un número de teléfono
        print(credential, pasw)
        query = self.client.table("credential").insert(
            {
                "email": credential,
                "password": pasw
            }
        ).execute()
        assert len(query.data) > 0
        user = query.data[0] if query.data else None
        if user:
            # Verificar la contraseña encriptada
            if checkpw(pasw.encode('utf-8'), user["password"].encode('utf-8')):
                return user
            else:
                return abort(400, description="La contraseña es incorrecta")
        else:
            return abort(404, description="El usuario no existe")
