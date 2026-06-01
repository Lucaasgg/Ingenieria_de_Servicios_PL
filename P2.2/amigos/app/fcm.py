import os
import firebase_admin
from firebase_admin import credentials, messaging

cred = None
try:
    json_path = os.path.join(os.path.dirname(__file__), '..', 'serviceAccount.json')
    cred = credentials.Certificate(json_path)
    firebase_admin.initialize_app(cred)
    print("Firebase inicializado correctamente")
except Exception as e:
    print(f"Error inicializando Firebase: {e}")
    cred = None

def notificar_amigos(tokens, body):
    if not tokens or cred is None:
        print("No hay tokens o Firebase no inicializado, no se envia notificacion")
        return
    try:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title="Amigos",
                body=body
            ),
            tokens=tokens
        )
        response = messaging.send_each_for_multicast(message)
        print(f"Notificacion enviada: {response.success_count} exitos, {response.failure_count} fallos")
    except Exception as e:
        print(f"Error enviando notificacion FCM: {e}")
