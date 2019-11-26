import argparse
import asyncio

import aiohttp
import uvloop

from modules.webapp import WebApp

# Set event loop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Set args parser
parser = argparse.ArgumentParser(description='Spotifast Bot')
parser.add_argument('--host', help='Host to listen', default='localhost')
parser.add_argument('--port', help='Port to accept connections', default='8080')
args = parser.parse_args()

# Initialize web application
web_app = WebApp()

if __name__ == '__main__':
    aiohttp.web.run_app(web_app.app, host=args.host, port=args.port)
