from http.server import BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import os
import json
from utils import write_json, read_html, render_template, FILE_PATH


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        if parsed_url.path == "/":
            self.send_html_file("index.html")
        elif parsed_url.path == "/message":
            self.send_html_file("message.html")
        elif parsed_url.path == "/read":
            self.send_read_page()
        else:
            if pathlib.Path().joinpath(parsed_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = dict(el.split("=") for el in data_parse.split("&"))

        write_json(data_dict)

        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def send_html_file(self, filename, status=200):
        """Sending a HTML-file as answer."""
        content = read_html(filename)
        if content:
            self.send_response(status)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def send_static(self):
        """Sending static files (CSS, JS, images)."""
        self.send_response(200)
        mime_type = mimetypes.guess_type(self.path)[0] or "text/plain"
        self.send_header("Content-type", mime_type)
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())

    def send_read_page(self):
        """Sending page with list of a messages"""
        messages = self.read_json()
        content = render_template("read.html", messages=messages)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content)

    def read_json(self):
        """Reading messages from data.json."""
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}
