#!/usr/bin/env python3

import sys
import http.server
import socketserver

__doc__ = """Usage: subgal host [options]
       subgal host --help

Serve files in current directory as a web server
for testing.

SECURITY WARNING: DON'T USE THIS UNLESS YOU ARE INSIDE A FIREWALL
-- it may execute arbitrary Python code or external programs.

Options:
  -p, --port=<port-number>  [DEFAULT: 8080]
  -h, --help                This help
""".format()


from docopt import docopt


def main(argv):
  args = docopt(__doc__, argv=argv)

  try:
    port = int(args["--port"])
  except ValueError as e:
    print("--port needs an integer")
    exit(1)

  Handler = http.server.SimpleHTTPRequestHandler

  with socketserver.TCPServer(("", port), Handler) as httpd:
    print(f"Serving at port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
  main(sys.argv)
