#!/usr/bin/env python

# Copyright (c) 2020 Jack Morris (jxmorris12@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import asyncio
import colorful
import sys
import os
import select
import shutil
import socket
import websockets

__version__ = '0.0.3'

SERVER_IP = 'www.spaste.io'
RECV_BUFFER_SIZE = 1024
READ_BUFFER_SIZE = 1024
SOCKET_TIMEOUT = 100 # seconds
DEFAULT_TERM_SIZE = (60, 20) # Default terminal width

def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--quiet', action='store_true',
            help='disable stdin passthrough')
    parser.add_argument('-i', '--ip', default=SERVER_IP,
            help='server IP address')
    parser.add_argument('-p', '--port', type=int, default=None,
            help='server port')
    parser.add_argument('-e', '--endpoint', type=str, default='/ws/chat/',
            help='server port')
    parser.add_argument('-d', '--delay', type=float, default=0,
            help='delay before starting to send data')
    return parser

def read1(stream):
    if hasattr(stream, 'read1'):
        return stream.read1(READ_BUFFER_SIZE)
    else:
        # XXX is there a better way to do this without doing a bunch of syscalls?
        buf = []
        while len(buf) < READ_BUFFER_SIZE:
            ready, _, _ = select.select([stream], [], [], 0) # poll
            if not ready:
                break
            data = stream.read(1)
            if not data:
                # even if we hit this case, it's fine: once we get to EOF, the
                # fd is always ready (and will always return "")
                break
            buf.append(data)
        return ''.join(buf)

def print_colored_url(data):
    # @TODO verify this is a URL, and if not, print error
    # in a different color, and exit.
    data = str(f'    {data}    ')
    terminal_size = shutil.get_terminal_size(DEFAULT_TERM_SIZE)
    columns = terminal_size.columns


    num_stars = min(len(data)+2, columns)
    
    def pc(s): print(colorful.bold_coral(s))
    
    pc('*' * num_stars)
    pc('*' + (' ' * len(data)) + '*')
    pc('*' + data + '*')
    pc('*' + (' ' * len(data)) + '*')
    pc('*' * num_stars)

async def async_main():
    if hasattr(sys.stdin, 'buffer'):
        stdin = sys.stdin.buffer
    else:
        stdin = os.fdopen(sys.stdin.fileno(), 'r', 0)
    stdout = sys.stdout.buffer if hasattr(sys.stdout, 'buffer') else sys.stdout
    stderr = sys.stderr.buffer if hasattr(sys.stderr, 'buffer') else sys.stderr

    try:
        parser = make_parser()
        args = parser.parse_args()

        if args.endpoint[0] == '/': 
            args.endpoint = args.endpoint[1:]

        if args.port:
            uri = f'ws://{args.ip}:{args.port}/{args.endpoint}'
        else:
            uri = f'ws://{args.ip}/{args.endpoint}'

        print(f'Connecting to {uri}...')

        conn = await websockets.connect(uri, timeout=SOCKET_TIMEOUT)

        print('got connection, waiting for data')
        # get URL from server first
        data = await conn.recv()

        print_colored_url(data.strip())

        # pipe data from stdin to server
        await asyncio.sleep(args.delay)
        async def check_server():
            # If the websocket is ready, print to stderr.
            while True:
                data = await conn.recv()
                print(data)
                stderr.write(data)
                stderr.flush()

        async def check_file():
            while True:
                # If stdin is ready, send data off to the server.
                # sys.stdin.isatty() returns false if there's something in stdin.
                if not stdin.isatty():
                    inp = read1(stdin)
                    if len(inp) == 0:
                        server_task.cancel()
                        break
                    await conn.send(inp)
                    if not args.quiet:
                        stdout.write(inp)
                        stdout.flush()

        # wrap in Task object
        # -> automatically attaches to event loop and executes
        file_task = asyncio.ensure_future(check_file())
        server_task = asyncio.ensure_future(check_server())

    except KeyboardInterrupt:
        # exit silently with an error code
        print('KeyboardInterrupt')
        exit(1)
    except socket.error as e:
        stderr.write(('websockets error: %s\n' % e).encode('utf8'))
        stderr.flush()
        # continue running
        while True:
            try:
                inp = read1(stdin)
                if len(inp) == 0:
                    # EOF
                    break
                if not args.quiet:
                    stdout.write(inp)
                    stdout.flush()
            except KeyboardInterrupt:
                exit(1)


def main():
    asyncio.get_event_loop().run_until_complete(async_main())

if __name__ == '__main__': main()