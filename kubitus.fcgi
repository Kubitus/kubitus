#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from kubitus import app

WSGIServer(app).run()

