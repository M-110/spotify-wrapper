"""Custom HTTP server"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import NoReturn, Type
from urllib.parse import parse_qs, urlsplit


def retrieve_authorization_code_using_local_http_server(
        server_flow_instance: 'PKCE') -> None:
    """Run a local HTTP server which Spotify will redirect to after the user
    authorizes the app, and then the server will receive the authorization
    code from the redirect and shut down.

    This will update the _authorization_code attribute of the server flow
    instance which called this function.

    server_flow_instance: The flow authorization instance that called this
        function.
    """
    server_address = server_flow_instance.server_address
    token_http_request_handler = create_request_handler(server_flow_instance)
    server = HTTPServer(server_address, token_http_request_handler)
    try:
        server.serve_forever()
    except:
        pass
    finally:
        server.server_close()


def create_request_handler(server_flow_instance
                           ) -> Type[BaseHTTPRequestHandler]:
    """This is to bypass all the init functions that the
    BaseHTTPRequestHandler and HTTPServer class/parent class's flow through."""

    class CustomTokenHandler(TokenHTTPRequestHandler):
        """A basic HTTPRequestHandler with a server_flow_instance injected
        into it."""
        def __init__(self, *args, **kwargs):
            self.server_flow_instance = server_flow_instance
            super().__init__(*args, **kwargs)

    return CustomTokenHandler


class TokenHTTPRequestHandler(BaseHTTPRequestHandler):
    """A temporary local server that will receive the token from
    Spotify. """
    server_flow_instance = None

    def do_GET(self) -> NoReturn:
        """Method called when a get request is made to the HTTP server.

        This will get a request when Spotify redirects the user to this url.
        The redirect request from spotifywrapper will contain a query that contains
        the authorization code. This will be saved to the server flow instance.

        Then an html response will be sent to the user saying the token was
        received.

        Raises:
            ValueError: If the CSRF token, state, does not match.
            KeyboardInterrupt: If everything is successful, this will be raised
                in order to shut down the server and continue on with the
                authorization flow.
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        query = parse_qs(urlsplit(self.path).query)

        if query['state'][0] != self.server_flow_instance.state:
            raise ValueError("State did not match.")

        self.server_flow_instance._authorization_code = query['code'][0]

        self.write_html_response()
        raise KeyboardInterrupt

    def write_html_response(self) -> None:
        # TODO: This could be prettier. Maybe use an html file.
        """Write the html response will which will be shown to the user to
        confirm that their code was received."""
        self.wfile.write(
            bytes("<h1>Token received. You may close this window.</h1>",
                  "utf-8"))

    def log_message(self, *_) -> None:
        """Override log method to disable requests being logged in the
        console."""
