from spyne import Application
from spyne.protocol import Soap11
from spyne.server.wsgi import WsgiApplication
from student_service import StudentService
from wsgiref.simple_server import make_server

soap_app = Application(
    [StudentService],
    tns='student.soap.api',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(soap_app)

if __name__=="__main__":
    print("[INFO] SOAP server running at http://localhost:8001/?wsdl")
    server = make_server('0.0.0.0', port=8002, app=wsgi_app)
    server.server_forver()
