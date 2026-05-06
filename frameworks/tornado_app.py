import tornado.ioloop
import tornado.web
import tornado.httpserver
import concurrent.futures
import time
import json

executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)


def cpu_intensive_task(iterations: int = 15_000_000) -> float:
    total = 0
    for i in range(iterations):
        total += i
    return total


class CPUBoundHandler(tornado.web.RequestHandler):
    """Блокирующий режим — выполняется в основном потоке"""
    def get(self):
        iterations = int(self.get_argument('n', 15_000_000))
        start = time.time()
        result = cpu_intensive_task(iterations)
        elapsed = time.time() - start
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps({
            'result': result,
            'time_seconds': elapsed,
            'iterations': iterations,
            'mode': 'blocking'
        }))


class CPUFixedHandler(tornado.web.RequestHandler):
    """Неблокирующий режим — выгрузка в ThreadPoolExecutor."""
    async def get(self):
        iterations = 15_000_000
        start = time.time()

        loop = tornado.ioloop.IOLoop.current()
        result = await loop.run_in_executor(executor, cpu_intensive_task, iterations)

        elapsed = time.time() - start
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps({
            'result': result,
            'time_seconds': elapsed,
            'iterations': iterations,
            'mode': 'non-blocking'
        }))


class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps({'status': 'ok'}))


def make_app():
    return tornado.web.Application([
        (r"/cpu", CPUBoundHandler),
        (r"/cpu_fixed", CPUFixedHandler),
        (r"/health", HealthHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8888)
    print("Tornado server running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()