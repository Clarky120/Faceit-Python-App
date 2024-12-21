from faceit import FaceitStats
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
import os
import json
from urllib.parse import urlparse, parse_qs

load_dotenv()


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == "/getMatchesForPlayer":
            parsed_url = urlparse(self.path)
            nickname = parse_qs(parsed_url.query)["nickname"][0]
            if len(nickname) == 0:
                self.send_response(400)
                self.end_headers()

            faceit = FaceitStats
            output = faceit.user_stats(nickname)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(output).encode("utf-8"))


def main():
    port = os.getenv("port")
    server = HTTPServer(("", int(port)), RequestHandler)
    print("SERVER RUNNING ON PORT %s" % port)
    server.serve_forever()


if __name__ == "__main__":
    main()