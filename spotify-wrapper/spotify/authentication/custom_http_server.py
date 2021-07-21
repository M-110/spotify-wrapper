"""Custom HTTP server"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlsplit


def run_server(server_flow_instance, server_address):
    """."""
    token_http_request_handler = create_request_handler(server_flow_instance)
    server = HTTPServer(server_address, token_http_request_handler)
    try:
        server.serve_forever()
    except:
        server.server_close()


def create_request_handler(server_flow_instance):
    """This is to bypass all the init functions that the
    BaseHTTPRequestHandler and HTTPServer class/parent class's flow through."""

    class CustomTokenHandler(TokenHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.server_flow_instance = server_flow_instance
            super().__init__(*args, **kwargs)

    return CustomTokenHandler


class TokenHTTPRequestHandler(BaseHTTPRequestHandler):
    """A temporary local server that will receive the token from
    Spotify. """
    server_flow_instance = None

    def do_GET(self):
        """Method called when a get request is made to the HTTP server."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        query = parse_qs(urlsplit(self.path).query)

        if query['state'][0] != self.server_flow_instance.state:
            raise ValueError("State did not match.")

        self.server_flow_instance.authorization_code = query['code'][0]

        self.write_html_response()
        raise KeyboardInterrupt

    def write_html_response(self):
        """Write the html response will which will be shown to the user to
        confirm that their code was received."""
        self.wfile.write(
            bytes("<h1>Token received. You may close this window.</h1>",
                  "utf-8"))

    def log_message(self, *_):
        """Override log method to disable requests being logged in the
        console."""
