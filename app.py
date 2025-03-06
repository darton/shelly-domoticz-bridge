from flask import Flask, request, jsonify
import logging
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Logger configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

USERNAME = 'domoticzlogin'
PASSWORD = 'apipasswd'

@app.before_request
def log_request_info():
    app.logger.debug('--- New Request ---')
    app.logger.debug('Method: %s', request.method)
    app.logger.debug('URL: %s', request.url)
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

@app.route('/execute_url', methods=['GET'])
def execute_url():
    type_ = request.args.get('type')
    param = request.args.get('param')
    idx = request.args.get('idx')
    switchcmd = request.args.get('switchcmd')
    nvalue = request.args.get('nvalue')

    # Construct URL
    base_url = 'http://127.0.0.1:8080/json.htm'
    if switchcmd:
        url = f'{base_url}?type={type_}&param={param}&idx={idx}&switchcmd={switchcmd}'
    else:
        url = f'{base_url}?type={type_}&param={param}&idx={idx}&nvalue={nvalue}'

    # Send HTTP request with basic authentication
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))

    if response.status_code == 200:
        #app.logger.info('Request executed successfully')
        return jsonify(response.json())
    else:
        #app.logger.error('Error executing request: %s, %s', response.status_code, response.text)
        return jsonify({'error': response.status_code, 'message': response.text}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
