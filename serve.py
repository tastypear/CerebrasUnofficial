# coding:utf-8
import argparse
import requests
import json
import os
from cerebras import CerebrasUnofficial
from flask import Flask, request, Response, stream_with_context, jsonify
import sys

# -- Start of Config --

# Replace with your cerebras.ai session token found in the `authjs.session-token` cookie.
# Or you can `set AUTHJS_SESSION_TOKEN=authjs.session-token`
# This token is valid for one month.
authjs_session_token = '12345678-abcd-abcd-abcd-12345678abcd'

# Replace with any string you wish like `my-api-key`.
# Or you can `set SERVER_API_KEY=my-api-key`
# You should set it to update the session token in the future.
server_api_key = 'my-api-key'

# -- End of Config --

sys.tracebacklimit = 0

authjs_session_token = os.environ.get('AUTHJS_SESSION_TOKEN', authjs_session_token)
server_api_key = os.environ.get('SERVER_API_KEY', server_api_key)
print(f'Using the cookie: authjs.session-token={authjs_session_token}')
print(f'Your api key: {server_api_key}')

cerebras_ai = CerebrasUnofficial(authjs_session_token)

app = Flask(__name__)
app.json.sort_keys = False
parser = argparse.ArgumentParser(description='Cerebras.AI API')
parser.add_argument('--host', type=str, help='Set the ip address.(default: 0.0.0.0)', default='0.0.0.0')
parser.add_argument('--port', type=int, help='Set the port.(default: 7860)', default=7860)
args = parser.parse_args()

class Provider:
    key = ''
    max_tokens = None
    api_url = ''

    def __init__(self, request_key, model):
        self.request_key = request_key
        self.model = model
        self.init_request_info()

    def init_request_info(self):
        if self.request_key == server_api_key:
            self.api_url = cerebras_ai.api_url
            self.key = cerebras_ai.get_api_key()

@app.route('/api', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    return f'''
        renew/change token by visiting:<br>
        {request.host_url}renew?key={{your server api key}}&token={{your Cerebras authjs_session_token}}<br>
        <br>
        Your interface:<br>
        {request.host_url}v1/chat/completions OR<br>
        {request.host_url}api/v1/chat/completions<br>
        <br>
        For more infomation by visiting:<br>
        https://github.com/tastypear/CerebrasUnofficial
    '''

@app.route('/api/renew', methods=['GET', 'POST'])
@app.route('/renew', methods=['GET', 'POST'])
def renew_token():
    if server_api_key == request.args.get('key', ''):
        request_token = request.args.get('token', '')
        global cerebras_ai
        cerebras_ai = CerebrasUnofficial(request_token)
        return f'new authjs.session_token: {request_token}'
    else:
        raise Exception('invalid api key')

@app.route('/api/v1/models', methods=['GET', 'POST'])
@app.route('/v1/models', methods=['GET', 'POST'])
def model_list():
    model_list = {
        'object': 'list',
        'data': [{
            'id': 'llama3.1-8b',
            'object': 'model',
            'created': 1721692800,
            'owned_by': 'Meta'
        }, {
            'id': 'llama-3.3-70b',
            'object': 'model',
            'created': 1733443200,
            'owned_by': 'Meta'
        }, {
            'id': 'deepseek-r1-distill-llama-70b',
            'object': 'model',
            'created': 1733443200,
            'owned_by': 'deepseek'
        }]
    }
    return jsonify(model_list)


@app.route('/api/v1/chat/completions', methods=['POST'])
@app.route('/v1/chat/completions', methods=['POST'])
def proxy():
    request_key = request.headers['Authorization'].split(' ')[1]
    if server_api_key != request_key:
        raise Exception('invalid api key')

    headers = dict(request.headers)
    headers.pop('Host', None)
    headers.pop('Content-Length', None)

    headers['X-Use-Cache'] = 'false'
    model = request.get_json()['model']
    provider = Provider(request_key, model)
    headers['Authorization'] = f'Bearer {provider.key}'
    chat_api = f'{provider.api_url}/v1/chat/completions'

    def generate():
        with requests.post(chat_api, json=request.json, headers=headers, stream=True) as resp:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    chunk_str = chunk.decode('utf-8')
                    yield chunk_str
    return Response(stream_with_context(generate()), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(host=args.host, port=args.port, debug=True)
