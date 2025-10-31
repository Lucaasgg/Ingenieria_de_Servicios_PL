import dns.resolver

respuesta = dns.resolver.query('apple.com')
print(respuesta)
for i in respuesta:
    print(i.address)
