import dns.resolver

respuesta = dns.resolver.resolve('en.wikipedia.org')
print(respuesta.response.to_wire())
