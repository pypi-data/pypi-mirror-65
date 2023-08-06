"""Renders vital stats about a single App Engine instance.

Intended for developers, not users. Uses the Runtime API:
https://developers.google.com/appengine/docs/python/backends/runtimeapi

Note that the Runtime API isn't implemented in dev_appserver, so all stats will
be reported as 0.

(The docs say it's deprecated because it's part of Backends, which is replaced
by Modules, but I haven't found a corresponding part of the Modules API.)

To turn on concurrent request recording, add the middleware and InfoHandler to your WSGI application, eg:

  from oauth_dropins.webutil.instance_info import concurrent_requests_wsgi_middleware, InfoHandler

  application = concurrent_requests_wsgi_middleware(webapp2.WSGIApplication([
      ...
      ('/_info', InfoHandler),
  ])
"""
import collections
import datetime
import heapq
import os
import threading

import webapp2

from . import handlers

CONCURRENTS_SIZE = 20

# A time when there was more than one request running at once. count is the
# first field so that instances compare by count, since they're stored in a
# heap, so that we keep the highest count instances.
Concurrent = collections.namedtuple('Concurrent', ('count', 'when'))

# globals
current_requests = set()  # stores string request IDs
current_requests_lock = threading.Lock()
concurrents = []  # a heapq. stores Concurrents


class InfoHandler(handlers.TemplateHandler):

  def template_file(self):
    return os.path.join(os.path.dirname(__file__),
                        'templates/instance_info.html')

  def template_vars(self):
    return {'concurrents': concurrents,
            'current_requests': current_requests,
            'os': os,
            'runtime': os.getenv('GAE_RUNTIME'),
            }


def concurrent_requests_wsgi_middleware(app):
  """WSGI middleware for per request instance info instrumentation.

  Follows the WSGI standard. Details: http://www.python.org/dev/peps/pep-0333/
  """
  def wrapper(environ, start_response):
    req_id = os.environ['REQUEST_LOG_ID']

    global current_requests, current_requests_lock, concurrents
    with current_requests_lock:
      current_requests.add(req_id)
      if len(current_requests) > 1:
        heapq.heappush(concurrents, Concurrent(count=len(current_requests),
                                               when=datetime.datetime.now()))
        if len(concurrents) > CONCURRENTS_SIZE:
          heapq.heappop(concurrents)

    ret = app(environ, start_response)

    with current_requests_lock:
      current_requests.remove(req_id)
    return ret

  return wrapper
