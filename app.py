import cherrypy
import socket
import boto3

'''function that shows current hostname'''
def show_server_hostname():
    return socket.gethostname()

'''Get all items from dynamodb table'''
def get_all_items():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('application_table')
    response = table.scan()
    return response['Items']

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        output_text = "Hostname:" + show_server_hostname() +"<br>\n"
        output_text += "Items:" + str(get_all_items())        
        return output_text

cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(HelloWorld())