import dns.resolver

respuesta = dns.resolver.resolve('apple.com')
print(respuesta)
for i in respuesta:
    print(i.address)
