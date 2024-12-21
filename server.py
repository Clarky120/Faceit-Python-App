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
            params = parse_qs(parsed_url.query)
            if "nickname" in params:
                nickname = parse_qs(parsed_url.query)["nickname"][0]
                faceit = FaceitStats
                output = faceit.user_stats(nickname)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(output).encode("utf-8"))
            else:
                self.send_response(400)
                self.end_headers()
        if parsed_url.path == "/getMatchRoom":
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)
            if "roomid" in params:
                room_id = parse_qs(parsed_url.query)["roomid"][0]
                faceit = FaceitStats
                output = faceit.match_room(room_id)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(output).encode("utf-8"))


def main():
    port = os.getenv("port")
    server = HTTPServer(("", int(port)), RequestHandler)
    print("SERVER RUNNING ON PORT %s" % port)
    server.serve_forever()


if __name__ == "__main__":
    main()
