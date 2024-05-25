from spyne import Application, rpc, ServiceBase, String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import requests

class solicitudSOAP(ServiceBase):
    @rpc(String, String, _returns=String)
    def register(self, email, password):
        # Construir la solicitud GraphQL
        url = 'http://unconnect-ag-rp:81/graphql'
        headers = {'Content-Type': 'application/json'}
        query = '''
        mutation {
          createAuthUser(email: "%s", password: "%s", role: USUARIO_REGULAR) {
            id
            email
            role
          }
        }
        ''' % (email, password)
        request_data = {'query': query}

        # Enviar la solicitud GraphQL
        response = requests.post(url, json=request_data, headers=headers)

        # Devolver la respuesta como un string
        return response.text

# Crear la aplicación SOAP
application = Application([solicitudSOAP], 'http://example.com/register',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

# Crear el servidor WSGI
wsgi_application = WsgiApplication(application)

# Ejecutar el servidor en el puerto 8082
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8082, wsgi_application)
    print("Servidor SOAP iniciado en http://localhost:8082")
    server.serve_forever()
