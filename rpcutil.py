from xmlrpc import client as xmlrpc_client
from xmlrpc.server import SimpleXMLRPCDispatcher
import pyspider
def connect_rpc(ctx, param, value):
    if not value:
        return
    return xmlrpc_client.ServerProxy(value, allow_none=True)









class WSGIXMLRPCApplication(object):
    """Application to handle requests to the XMLRPC service"""

    def __init__(self, instance=None, methods=None):
        """Create windmill xmlrpc dispatcher"""
        if methods is None:
            methods = []
        try:
            self.dispatcher = SimpleXMLRPCDispatcher(allow_none=True, encoding=None)
        except TypeError:
            # python 2.4
            self.dispatcher = SimpleXMLRPCDispatcher()
        if instance is not None:
            self.dispatcher.register_instance(instance)
        for method in methods:
            self.dispatcher.register_function(method)
        self.dispatcher.register_introspection_functions()

    def register_instance(self, instance):
        return self.dispatcher.register_instance(instance)

    def register_function(self, function, name=None):
        return self.dispatcher.register_function(function, name)

    def handler(self, environ, start_response):
        """XMLRPC service for windmill browser core to communicate with"""

        if environ['REQUEST_METHOD'] == 'POST':
            return self.handle_POST(environ, start_response)
        else:
            start_response("400 Bad request", [('Content-Type', 'text/plain')])
            return ['']

    def handle_POST(self, environ, start_response):
        """Handles the HTTP POST request.

        Attempts to interpret all HTTP POST requests as XML-RPC calls,
        which are forwarded to the server's _dispatch method for handling.

        Most code taken from SimpleXMLRPCServer with modifications for wsgi and my custom dispatcher.
        """

        try:
            # Get arguments by reading body of request.
            # We read this in chunks to avoid straining
            # socket.read(); around the 10 or 15Mb mark, some platforms
            # begin to have problems (bug #792570).

            length = int(environ['CONTENT_LENGTH'])
            data = environ['wsgi.input'].read(length)
            print('-------wsgi----data')
            print(data)
            # In previous versions of SimpleXMLRPCServer, _dispatch
            # could be overridden in this class, instead of in
            # SimpleXMLRPCDispatcher. To maintain backwards compatibility,
            # check to see if a subclass implements _dispatch and
            # using that method if present.
            response = self.dispatcher._marshaled_dispatch(
                data, getattr(self.dispatcher, '_dispatch', None)
            )
            response += b'\n'
        except Exception as e:  # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            print(e)
            start_response("500 Server error", [('Content-Type', 'text/plain')])
            return []
        else:
            # got a valid XML RPC response
            start_response("200 OK", [('Content-Type', 'text/xml'), ('Content-Length', str(len(response)),)])
            return [response]

    def __call__(self, environ, start_response):
        print(environ)
        return self.handler(environ, start_response)





if __name__ == '__main__':
    pass




