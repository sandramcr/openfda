import webserver
import socketserver


#WEB SERVER: codigo fuera de las clases
PORT=8092
#Handler = http.server.SimpleHTTPRequestHandler #Clase con objetos para gestionar las respuestas
Handler = webserver.testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
