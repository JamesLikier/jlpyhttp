import httpserver
import socket

s = httpserver.httpserver("localhost",80)

@s.register(("GET","POST"),"/")
def root(req: httpserver.httprequest, sock: socket.socket):
    with open("main.html","rb") as f:
        resp = httpserver.httpresponse()
        resp.body = f.read()
        resp.statuscode = 200
        resp.send(sock)

@s.register(("GET","POST"),"/multipart?raw")
def multipartraw(req: httpserver.httprequest, sock: socket.socket):
    with open("multipartform.html","rb") as f:
        resp = httpserver.httpresponse()
        resp.body = f.read().replace(b'@placeholder', str(req.raw).encode())
        resp.statuscode = 200
        resp.send(sock)

@s.register(("GET","POST"),"/multipart?body")
def multipartbody(req: httpserver.httprequest, sock: socket.socket):
    with open("multipartform.html","rb") as f:
        resp = httpserver.httpresponse()
        resp.body = f.read().replace(b'@placeholder',str(req.body).encode())
        resp.statuscode = 200
        resp.send(sock)

@s.registerstatic("/static/")
def static(req: httpserver.httprequest, sock: socket.socket):
    resp = httpserver.httpresponse()
    try:
        if req.uri.find("./") > -1:
            raise Exception
        with open("."+req.uri, "rb") as f:
            resp.body = f.read()
            resp.statuscode = 200
    except:
        resp.statuscode = 404
    resp.send(sock)

print("Starting server...\n")
s.start()