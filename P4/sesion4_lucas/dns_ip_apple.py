import dns.resolver

def obtener_ips(dominio):
    try:
        respuestas = dns.resolver.resolve(dominio, 'A')  # Consulta registros tipo A (IPv4)
        print(f"Direcciones IP para {dominio}:")
        for respuesta in respuestas:
            print(respuesta.to_text())
    except dns.resolver.NXDOMAIN:
        print(f"El dominio {dominio} no existe.")
    except dns.resolver.NoAnswer:
        print(f"No se encontraron registros A para {dominio}.")
    except dns.resolver.Timeout:
        print("La consulta DNS ha expirado.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    obtener_ips("apple.com")