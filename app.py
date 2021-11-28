import cherrypy
import socket
import boto3
import requests

'''funtion to get current region'''
def get_region():
    r = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document")
    response_json = r.json()
    return response_json.get('region')

'''function that shows current hostname'''
def show_server_hostname():
    return socket.gethostname()

'''Get all items from dynamodb table'''
def get_all_items(table_name):
    dynamodb = boto3.resource('dynamodb',region_name=get_region())
    table = dynamodb.Table('application_table')
    response = table.scan()
    return response['Items']

def get_table_name():
    with open("/var/application/config.db") as f:
        s = f.read()
    
    return s.split("/")[-1].replace("\n","").replace(" ","")
class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        output_text = "Hostname:" + show_server_hostname() +"<br>\n"       
        output_text += "Tablename:" + get_table_name() + "<br>\n"
        output_text += "Items:" + str(get_all_items(get_table_name()))        
        return output_text


cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(HelloWorld())