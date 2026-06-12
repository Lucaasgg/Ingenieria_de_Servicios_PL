# coding: utf-8
import logging
import getpass
import os
import ssl
import slixmpp

class MiBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.callback_para_session_start)
        self.add_event_handler("message", self.callback_para_message)
        self.add_event_handler("chatstate_composing", self.callback_composing)
        self.add_event_handler("chatstate_paused", self.callback_paused)
        self.add_event_handler("chatstate_active", self.callback_active)

    async def callback_para_session_start(self, event):
        print("Sesion iniciada!")
        self.send_presence()
        await self.get_roster()
        print("Roster recibido.")

    async def callback_para_message(self, event):
        recibido = event["body"]
        print(f"Recibido tipo {event['type']} de {event['from']}: {recibido}")
        if event["type"] == "chat":
            if recibido.startswith("="):
                try:
                    respuesta = str(eval(recibido[1:]))
                except Exception as e:
                    respuesta = f"Error: {e}"
            else:
                respuesta = f"?{recibido}?"
            msg = self.Message()
            msg["to"] = event["from"]
            msg["type"] = "chat"
            msg["body"] = respuesta
            msg["chat_state"] = "active"
            msg.send()

    async def callback_composing(self, event):
        print(f"{event['from'].bare} esta escribiendo...")

    async def callback_paused(self, event):
        print(f"{event['from'].bare} ha parado de escribir")

    async def callback_active(self, event):
        print(f"{event['from'].bare} esta activo")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")
    jid = "bot@ingserv456"
    ip = "localhost"
    port = 5222
    clave = "bot" 
    if clave is None:
        clave = getpass.getpass("Contrasena: ")
    cert_file = "../etc/prosody/certs/ingserv456.crt"
    ssl_context = ssl.create_default_context()
    if os.path.exists(cert_file):
        ssl_context.load_verify_locations(cert_file)
        ssl_context.check_hostname = False
    else:
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
    client = MiBot(jid, clave)
    client.register_plugin("xep_0085")
    client.ssl_context = ssl_context
    client.connect((ip, port))
    client.process(forever=True)
