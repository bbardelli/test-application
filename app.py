import cherrypy
import socket
import boto3
import requests
import os

'''funtion to get current region'''
def get_region():
    r = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document")
    response_json = r.json()
    return response_json.get('region')

'''function that shows current hostname'''
def show_server_hostname():
    return socket.gethostname()

'''Get all items from dynamodb table'''
def get_all_items():
    dynamodb = boto3.resource('dynamodb',region_name=get_region())
    table = dynamodb.Table('application_table')
    response = table.scan()
    return response['Items']

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        output_text = "Hostname:" + show_server_hostname() +"<br>\n"
        output_text += "Items:" + str(get_all_items())        
        output_text += "<br>\n Env-Vars: <br>\n"
        output_text += "<br>\n".join([x + "=" + os.environ[x] for x in os.environ])
        return output_text


cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(HelloWorld())