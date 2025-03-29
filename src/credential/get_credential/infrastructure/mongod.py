from ....mongodb.connect import ConnectionMongo
from bcrypt import checkpw
from flask import abort

class MongodCredential:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def CredentialConnect(self, credential, pasw):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["credential"]
        # Verificar si creditial es un email o un número de teléfono
        print(credential, pasw)
        if not isinstance(credential, int):  # Es un correo electrónico
            user = col.find_one({"email": credential})
        else:  # Se asume que es un número de teléfono
            user = col.find_one({"cel_number": credential})
        if user:
            # Verificar la contraseña encriptada
            if checkpw(pasw.encode('utf-8'), user["password"] if isinstance(user["password"], str) else user["password"]):
                return user
            else:
                return abort(400, description="La contraseña es incorrecta")
        else:
            return abort(404, description="El usuario no existe")
