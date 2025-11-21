import logging
import getpass
import os
import ssl

class MyBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.add_event_handler("session_start", self.callback_para_session_start)
        self.add_event_handler("message", self.callback_para_message)

    async def callback_para_session_start(self, event):
        print("Sesión iniciada!")
        self.send_presence()
        await self.get_roster()
        print("Roster recibido.")

    async def callback_para_message(self, event):
        recibido = event['body']
        print(f"Recibido un mensaje de tipo {event['type']} de {event['from']}")
        print(f"Que dice: {recibido}")

        if event["type"] == "chat":
            msg = self.Message()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')

    jid = "bot@ingserv00"
    ip = "localhost"
    port = 5222
    clave = os.environ.get("CLAVEBOT")
    if clave is None:
        clave = getpass.getpass("Contraseña: ")

    cert_file = "./etc/prosody/certs/ingserv00.crt"
    ssl_context = ssl.create_default_context()

    if os.path.exists(cert_file):
        print(f"Cargando certificado de confianza desde: {cert_file}")
        ssl_context.load_verify_locations(cert_file)
        
        print("Desactivando la comprobación de hostname.")
        ssl_context.check_hostname = False
    else:
        print(f"ADVERTENCIA: No se encontró '{cert_file}'. Desactivando TODA la validación de certificado.")
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

    client = MyBot(jid, clave)

    client.ssl_context = ssl_context
    
    client.connect((ip, port))
    
    client.process(forever=True)
