import logging
logger = logging.getLogger(__file__)

class Processer(object):
    def __init__(self,inqueue, status_queue, newtask_queue, result_queue,):
        self.inqueue = inqueue
        self.status_queue = status_queue
        self.newtask_queue = newtask_queue
        self.result_queue = result_queue
        self._quit = False

    def run(self):
        while not self._quit:
            task, response = self.inqueue.get()
            self.on_task(task, response)

    def on_task(self,task, response):
        print("on_task")


class Fetcher(object):
    def __init__(self,inqueue,outqueue):
        self.inqueue = inqueue
        self.outqueue = outqueue


    def run(self):
        while True:
            task = self.inqueue.get()
            self.fetch(task)

    def fetch(self,task):
        print(task)
        self.outqueue.put("fetchresult")

    def rpc_server(self):
        from rpcutil import WSGIXMLRPCApplication
        application = WSGIXMLRPCApplication()

        def sync_fetch(task):
            print("sync_fetch")
            return "sync_fetch"

        application.register_function(sync_fetch, 'fetch')
        import tornado.httpserver
        container = tornado.wsgi.WSGIContainer(application)
        xmlrpc_ioloop = tornado.ioloop.IOLoop()
        xmlrpc_server = tornado.httpserver.HTTPServer(container, io_loop=xmlrpc_ioloop)
        bind = "127.0.0.1"
        port = 3333
        xmlrpc_server.listen(port=port, address=bind)
        logger.info('fetcher.xmlrpc listening on %s:%s', bind, port)
        xmlrpc_ioloop.start()


class Scheduler(object):
    def __init__(self,taskqueue,outqueue):
        self.taskqueue = taskqueue
        self.outqueue = outqueue
        pass


    def run(self):
        while  True:
            self.taskqueue.put("scheduler task")

    def rpc_scheduler(self):
        from rpcutil import WSGIXMLRPCApplication
        application = WSGIXMLRPCApplication()

        def sync_scheduler(task):
            print("this is scheduler")
            return "this is scheduler"

        application.register_function(sync_scheduler, 'scheduler')
        import tornado.httpserver
        container = tornado.wsgi.WSGIContainer(application)
        xmlrpc_ioloop = tornado.ioloop.IOLoop()
        xmlrpc_server = tornado.httpserver.HTTPServer(container, io_loop=xmlrpc_ioloop)
        bind = "127.0.0.1"
        port = 2222
        xmlrpc_server.listen(port=port, address=bind)
        logger.info('Scheduler.xmlrpc listening on %s:%s', bind, port)
        xmlrpc_ioloop.start()










# rpc 分布式  再加个
# wsgi 运行了一个 rpc application
if __name__ == '__main__':
    import queue
    #  跑起来了
    # f = Fetcher(queue.Queue(),queue.Queue())
    # f.rpc_server()


    s = Scheduler(queue.Queue(),queue.Queue())
    s.rpc_scheduler()

#   调函数  xmlrpc  client 函数




#  simple










