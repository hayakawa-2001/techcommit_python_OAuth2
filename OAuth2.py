import urllib
from urllib import parse
import oauth2 as oauth
import webbrowser
import http.server
import socketserver
import urllib.parse as urlparse

request_token_url = 'https://twitter.com/oauth/request_token'
access_token_url = 'https://twitter.com/oauth/access_token'
authenticate_url = 'https://twitter.com/oauth/authorize'
callback_url = "http://localhost:8080/"
auth_url = 'https://twitter.com/oauth/authorize?oauth_token='

HOST = '127.0.0.1'
PORT = 8080

#Consumer_API_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
#Consumer_API_key_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'

def get_request_token():
    consumer = oauth.Consumer(key=Consumer_API_key, secret=Consumer_API_key_secret)
    client = oauth.Client(consumer)

    resp, content = client.request('%s?&oauth_callback=%s' % (request_token_url, callback_url))
    request_token = dict(parse_qsl(content.decode()))
    return request_token['oauth_token']

def parse_qsl(url):
    param = {}
    for i in url.split('&'):
        _p = i.split('=')
        param.update({_p[0]: _p[1]})
    return param

def get_access_token(oauth_token, oauth_verifier):
    consumer = oauth.Consumer(key=Consumer_API_key, secret=Consumer_API_key_secret)
    token = oauth.Token(oauth_token, oauth_verifier)

    client = oauth.Client(consumer, token)
    resp, content = client.request("https://api.twitter.com/oauth/access_token",
                                   "POST", body="oauth_verifier={0}".format(oauth_verifier))
    token = dict(parse_qsl(content.decode()))
    access_token = token['oauth_token']
    token_secret = token['oauth_token_secret']
    return (access_token, token_secret)

request_token = get_request_token()
#print(request_token)
authorize_url = '%s?oauth_token=%s' % (authenticate_url, request_token)
#print(authorize_url)
webbrowser.open(authorize_url)

class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(b"<h1>Authenticated</h1>")

        #print(self.path)
    
        parsedurl = urlparse.urlparse(self.path)
        self.server.return_oauth_token = urlparse.parse_qs(parsedurl.query)['oauth_token'][0]
        self.server.return_oauth_verifier =  urlparse.parse_qs(parsedurl.query)['oauth_verifier'][0]


with socketserver.TCPServer((HOST, PORT), ServerHandler) as httpd:
    print("http server start")
    #httpd.serve_forever()
    httpd.handle_request()
    oauth_token = httpd.return_oauth_token
    oauth_verifier = httpd.return_oauth_verifier
    print("oauth_token = ",oauth_token)
    print("oauth_verifier = ",oauth_verifier)
    print("http server shutdown")

access_token, token_secret = get_access_token(oauth_token, oauth_verifier)
print("access_token = ",access_token)
print("token_secret = ",token_secret)
