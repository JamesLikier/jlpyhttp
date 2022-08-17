import httpserver
import socket
from re import Match

s = httpserver.httpserver("localhost",80)

@s.register(("GET","POST"),"/$")
def root(req: httpserver.httprequest, match: Match, sock: socket.socket):
    with open("main.html","rb") as f:
        resp = httpserver.httpresponse()
        resp.body = f.read()
        resp.statuscode = httpserver.statuscodes.OK
        resp.send(sock)

@s.register(("GET","POST"),"/multipart\?raw$")
def multipartraw(req: httpserver.httprequest, match: Match, sock: socket.socket):
    with open("multipartform.html","rb") as f:
        resp = httpserver.httpresponse()
        resp.body = f.read().replace(b'@placeholder', str(req.raw).encode())
        resp.statuscode = httpserver.statuscodes.OK
        resp.send(sock)

@s.register(("GET","POST"),"/multipart\?body$")
def multipartbody(req: httpserver.httprequest, match: Match, sock: socket.socket):
    with open("multipartform.html","rb") as f:
        resp = httpserver.httpresponse()
        resp.body = f.read().replace(b'@placeholder',str(req.body).encode())
        resp.statuscode = httpserver.statuscodes.OK
        resp.send(sock)

@s.register(("GET","POST"),"/multipart/form$")
def multipartform(req: httpserver.httprequest, match: Match, sock: socket.socket):
    with open("multipartform.html","rb") as f:
        resp = httpserver.httpresponse(httpserver.statuscodes.OK)
        resp.body = f.read().replace(b'@placeholder',str(req.form.data).encode())
        resp.send(sock)

@s.register(("GET","POST"),"/multipart/format/form$")
def multipartbody(req: httpserver.httprequest, match: Match, sock: socket.socket):
    with open("multipartform.html","rb") as f:
        resp = httpserver.httpresponse()
        lines = []
        lines.append(b'<br/>')
        lines.append(req.form.format())
        lines.append(b'<br/>')
        lines.append(b'<br/>')
        lines.append(req.body)
        lines.append(b'<br/>')
        lines.append(b'<br/>')
        lines.append(str(req.body == req.form.format()).encode())
        resp.body = f.read().replace(b'@placeholder',str(b''.join(lines)).encode())
        resp.statuscode = httpserver.statuscodes.OK
        resp.send(sock)

@s.register(("GET","POST"),"/multipart/format$")
def multipartformat(req: httpserver.httprequest, match: Match, sock: socket.socket):
    with open("multipartform.html","rb") as f:
        resp = httpserver.httpresponse()
        lines = []
        lines.append(b'<br/>')
        lines.append(req.format())
        lines.append(b'<br/>')
        lines.append(b'<br/>')
        lines.append(req.raw)
        lines.append(b'<br/>')
        lines.append(b'<br/>')
        lines.append(str(req.raw == req.format()).encode())
        resp.body = f.read().replace(b'@placeholder',str(b''.join(lines)).encode())
        resp.statuscode = httpserver.statuscodes.OK
        resp.send(sock)

@s.register(("GET","POST"),"/urlenc\?form$")
def urlencform(req: httpserver.httprequest, match: Match, sock: socket.socket):
    with open("urlencform.html","rb") as f:
        resp = httpserver.httpresponse()
        lines = []
        lines.append(b'<br/>')
        lines.append(req.form.format())
        lines.append(b'<br/>')
        lines.append(b'<br/>')
        lines.append(req.body)
        lines.append(b'<br/>')
        lines.append(b'<br/>')
        lines.append(str(req.body == req.form.format()).encode())
        resp.body = f.read().replace(b'@placeholder',str(b''.join(lines)).encode())
        resp.statuscode = httpserver.statuscodes.OK
        resp.send(sock)

@s.register(("GET","POST"),"/urlenc$")
def urlenc(req: httpserver.httprequest, match: Match, sock: socket.socket):
    with open("urlencform.html","rb") as f:
        resp = httpserver.httpresponse()
        resp.body = f.read().replace(b'@placeholder',str(req.raw).encode())
        resp.statuscode = httpserver.statuscodes.OK
        resp.send(sock)

@s.register(("GET","POST"),"/urlenc/format$")
def urlencformat(req: httpserver.httprequest, match: Match, sock: socket.socket):
    with open("urlencform.html","rb") as f:
        resp = httpserver.httpresponse()
        lines = []
        lines.append(b"<br/>")
        lines.append(req.format())
        lines.append(b"<br/>")
        lines.append(b"<br/>")
        lines.append(req.raw)
        lines.append(b"<br/>")
        lines.append(b"<br/>")
        lines.append(str(req.raw == req.format()).encode())
        resp.body = f.read().replace(b'@placeholder',str(b''.join(lines)).encode())
        resp.statuscode = httpserver.statuscodes.OK
        resp.send(sock)

@s.registerstatic("/static/.*")
def static(req: httpserver.httprequest, match: Match, sock: socket.socket):
    resp = httpserver.httpresponse()
    try:
        if req.uri.find("./") > -1:
            raise Exception
        with open("."+req.uri, "rb") as f:
            resp.body = f.read()
            resp.statuscode = httpserver.statuscodes.OK
    except:
        resp.statuscode = httpserver.statuscodes.NOT_FOUND
    resp.send(sock)

print("Starting server...\n")
s.start()