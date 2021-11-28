import cherrypy
import socket

'''function that shows current hostname'''
def show_server_hostname():
    return socket.gethostname()



class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return show_server_hostname()

cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(HelloWorld())