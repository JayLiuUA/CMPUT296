#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright 2018 Eddie Antonio Santos <easantos@ualberta.ca>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Serves a webpage for writing GET requests, with a dynamic endpoint
for testing <form> inputs and AJAX requests.

Usage:

    python3 server.py

Then use an HTTP client to GET http://localhost:8000/calc/
"""

import http.server
import json
import traceback
import urllib.parse
from pathlib import Path


# Use this to access files relative to the directory that this script is
# placed in.
here = Path(__file__).absolute().parent


class BadRequest(Exception):
    """
    Raise this exception to prevent returning to the normal do_X handler.

    You MUST send a proper HTTP response before raising this error, however.
    """


class AJAXRequestHandler(http.server.BaseHTTPRequestHandler):
    """
    Defines a GET request handler: a static one and a dynamic one.

    Interesting attributes:

        .path       -- HTTP request target (path + query + fragment)
        .headers    -- dictionary of request headers names -> values
        .query      -- [defined by do_GET()] dictionary of query parameters
        .query_raw  -- [defined by do_GET()] the query string
        .wfile      -- write bytes of the response here!

    """

    def do_GET(self):
        """
        Handle a GET request to:

            /       -- index
            /calc/  -- calculator

        Respond with 404 for anything else.
        """

        # What BaseHTTPRequestHandler calls "path"
        # is actually the request target. i.e., path + query + fragment
        components = urllib.parse.urlparse(self.path)
        path = components.path
        self.query_raw = components.query
        self.query = urllib.parse.parse_qs(self.query_raw)

        if path == '/':
            self.do_GET_index()
        elif path == '/calc/':
            self.do_GET_calc()
        else:
            self.do_404()

    def do_GET_index(self):
        """
        Serve index.html. Responds with HTTP 404 if index.html does not
        exist in the same directory as this script.
        """
        try:
            with open(str(here / 'index.html'), 'rb') as index_file:
                body = index_file.read()
        except FileNotFoundError:
            return self.client_error(
                'You must create a page called index.html '
                'in the same directory as server.py',
                status_code=404
            )
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET_calc(self):
        """
        A simple calculator. Requires query parameters of 'a', 'b', and 'op'.
        'op' is '+', '-', '*', '/'; 'a' and 'b' will be parsed as floats.

        The response will depend on the Accept header.

        If any of the parameters are missing or invalid, this responds with
        HTTP 400 and a short, explanatory message.
        """
        a, b, op = self.parse_calc_query_params()

        try:
            answer = {
                '+': lambda: a + b,
                '-': lambda: a - b,
                '*': lambda: a * b,
                '/': lambda: a / b,
            }[op]()
        except Exception:
            # The user might try to divide by zero or something.
            return self.server_error(
                'Could not calculate {0} {2} {1}'.format(a, b, op)
            )

        # Perform content negotiation. Technically, I should be looking at the
        # q= values to prioritize which Content-Type to send back, but I'm too
        # lazy for that. Instead, try we'll prioritize application/json over
        # all other types, else assume html.
        accept_types = self.get_accept_types()
        if 'application/json' in accept_types:
            body = json.dumps({'answer': answer}).encode('UTF-8')
        elif 'text/html' in accept_types or '*/*' in accept_types:
            body = '<p> The answer is {0} </p>'.format(answer).encode('UTF-8')
        else:
            self.client_error(
                "Unsure what content type to send back given the accept "
                "header of " + repr(self.headers.get('Accept', '<not given>')),
                status_code=406  # "Not Acceptable"
            )

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def parse_calc_query_params(self):
        """
        Returns a, b, and op parameters from the query parameters.
        If any of them are missing or invalid, it responds with HTTP 400
        (Bad Request).
        """
        q = self.query

        # Make sure that all arguments are present in the query.
        if 'a' not in q or 'b' not in q or 'op' not in q:
            self.client_error(
                'Did not get proper query arguments! '
                'I expected ?a=...&b=...&op=... '
                'But I actually got {0}'.format(self.query_raw or 'nothing')
            )

        # We use the convection of using the *last* value if the argument is
        # specified multiple times.
        a, b, op = q['a'][-1], q['b'][-1], q['op'][-1]
        try:
            a = float(a)
            b = float(b)
        except ValueError:
            self.client_error(
                'Invalid value for a ({0!r}) and/or b ({1!r})'.format(a, b)
            )

        if op not in '+-/*':
            self.client_error(
                'Invalid value for op. It should be one of '
                "'+', '-', '*', '/' but actually got " + repr(op)
            )
        return a, b, op

    def get_accept_types(self):
        """
        Very crudely returns a list of the acceptable content-types as provided
        in the Accept request header.
        """
        accepts = self.headers.get('Accept', None)
        if accepts:
            # Let's ignore the q= parameter for Content-Types.
            return [mime.split(';')[0].strip() for mime in accepts.split(',')]
        else:
            # No Accept header? Assume the client will accept *anything*!
            return ['*/*']

    def do_404(self):
        """
        Responds with a simple 404.
        """
        self.send_response(404)
        self.end_headers()

    def client_error(self, err_msg, status_code=400):
        """
        Call this to respond with an HTTP 4xx client error.
        """
        body = str(err_msg).encode('UTF-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/plain; charset=UTF-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        raise BadRequest

    def server_error(self, err_msg='Server error! See logs'):
        """
        Call this when the server has an unhandled exception.

        This should be called within an except: clause.
        """
        # Print a traceback of the error to the logs so that we can actually
        # debug the dang error!
        traceback.print_exc()

        body = str(err_msg).encode('UTF-8')
        self.send_response(500)
        self.send_header('Content-Type', 'text/plain; charset=UTF-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    host, port = 'localhost', 8000
    server = http.server.HTTPServer((host, port), AJAXRequestHandler)
    print("Listening on \033[1mhttp://{0}:{1}/\033[m".format(host, port))
    print("Press ctrl+c to stop server.")
    server.serve_forever()
