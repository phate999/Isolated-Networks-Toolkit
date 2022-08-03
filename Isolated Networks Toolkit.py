# Web UI for Cradlepoint Isolated Networks

import cgi
from http.server import HTTPServer, SimpleHTTPRequestHandler
from http import HTTPStatus
import requests
import datetime
import json

routers = {}
ncos_file = None
license_file = None
config_file = None
admin_port = ':8080'

class WebServerRequestHandler(SimpleHTTPRequestHandler):
    """Handles all HTTP requests"""

    def do_GET(self):
        """Handles GET requests"""
        print('Received Get request: {}'.format(self.path))
        super().do_GET()

    def do_POST(self):
        """Handles POST requests"""
        global routers
        global ncos_file
        global license_file
        global config_file
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        for action in form.keys():
            file_data = None
            action_item = form[action]
            if action_item.filename:
                file_data = action_item.file.read()
            if action == 'routers':
                content = file_data.decode('UTF-8')
                routers = [x.split(',') for x in content.split('\r\n')]
                # If first character of first cell of first row is non-integer, assume it is header row and remove it
                try:
                    int(routers[0][0][0])
                except:
                    routers.pop(0)
                print('Received routers .csv file.')
            elif action == 'license':
                license_file = 'licenses/' + action_item.filename
                with open(license_file, 'wb') as f:
                    f.write(file_data)
                print(f'Received license file: {license_file}')
            elif action == 'ncos':
                ncos_file = 'NCOS/' + action_item.filename
                with open(ncos_file, 'wb') as f:
                    f.write(file_data)
                print('Received NCOS file.')
            elif action == 'config':
                config_file = 'configs/' + action_item.filename
                with open(config_file, 'wb') as f:
                    f.write(file_data)
                print('Received Configuration file.')
            elif action == 'go_license':
                push('feature')
            elif action == 'go_ncos':
                push('fw_upgrade')
            elif action == 'go_config':
                push('config_save')

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(json.dumps({'routers': routers,
                                     'license_file': bool(license_file),
                                     'ncos_file': bool(ncos_file)
                                     }).encode('UTF-8'))

def push(action):
    """Pushes file to each router"""
    # Get file
    filemap = {
        'feature': license_file,
        'fw_upgrade': ncos_file,
        'config_save': config_file
    }
    file = {'file': open(filemap[action], 'rb')}

    # Push file to routers and log results
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H.%M')
    with open(f'logs/IsoNet Logs {timestamp}.txt', 'wt') as log:
        print_log(log, f'Starting Action: {action}')
        for router in routers:
            ip_address = router[0]
            if not ':' in ip_address:
                ip_address += admin_port
            username = router[1]
            password = router[2]
            product_url = f'http://{ip_address}/api/status/product_info'
            system_id_url = f'http://{ip_address}/api/config/system/system_id'
            try:
                req = requests.get(product_url, auth=(username, password), verify=False, timeout=5)
                if req.status_code < 300:
                    req = req.json()
                    product_info = req['data']
                    system_id_req = requests.get(system_id_url, auth=(username, password), verify=False).json()
                    system_id = system_id_req["data"]
                    print_log(log, f'Connected to {system_id} at {ip_address}: {product_info["product_name"]} MAC: {product_info["mac0"]} SERIAL_NUM: {product_info["manufacturing"]["serial_num"]}')
                    url = f'http://{ip_address}/{action}'
                    try:
                        req = requests.post(url, files=file, auth=(username, password), verify=False)
                        if req.status_code < 300:
                            print_log(log, f'Successfully Pushed {filemap[action]} to {system_id }.')
                        else:
                            print_log(log, f'ERROR pushing {filemap[action]} to router {url}: {req.status_code} {req.text}')
                    except Exception as e:
                        print_log(log, f'Exception pushing {filemap[action]} to router {url}: {e}')
                else:
                    print_log(log, f'ERROR connecting to router {url}: {req.status_code} {req.text}')
            except Exception as e:
                print_log(log, f'Exception occurred when connecting to router {url}: {e}')

def print_log(log, msg):
    """Writes a timestamped log and prints the message"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = f'{timestamp} {msg}'
    log.write(msg + '\n')
    print(msg)

if __name__ == '__main__':
    print('Starting server on http://localhost:9000')
    server_address = ('localhost', 9000)
    httpd = HTTPServer(server_address, WebServerRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Stopping Server, Key Board interrupt')
