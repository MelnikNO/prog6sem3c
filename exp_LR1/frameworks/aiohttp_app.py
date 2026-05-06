from aiohttp import web
import asyncio
import concurrent.futures
import time

executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)


def cpu_intensive_task(iterations: int = 15_000_000) -> int:
    total = 0
    for i in range(iterations):
        total += i
    return total


async def cpu_bound(request):
    """Блокирующий режим"""
    try:
        iterations = int(request.query.get('n', 15_000_000))
    except:
        iterations = 15_000_000

    start = time.time()
    result = cpu_intensive_task(iterations)
    elapsed = time.time() - start
    return web.json_response({
        'result': result,
        'time_seconds': elapsed,
        'iterations': iterations,
        'mode': 'blocking (АНТИПАТТЕРН)'
    })


async def cpu_fixed(request):
    """Неблокирующий режим — правильный"""
    iterations = 15_000_000
    start = time.time()

    loop = asyncio.get_running_loop()
    try:
        result = await asyncio.wait_for(
            loop.run_in_executor(executor, cpu_intensive_task, iterations),
            timeout=30.0
        )
    except asyncio.TimeoutError:
        return web.json_response({'error': 'timeout'}, status=504)

    elapsed = time.time() - start
    return web.json_response({
        'result': result,
        'time_seconds': elapsed,
        'iterations': iterations,
        'mode': 'non-blocking (ThreadPoolExecutor)'
    })


async def health(request):
    return web.json_response({'status': 'ok'})


app = web.Application()
app.router.add_get('/cpu', cpu_bound)
app.router.add_get('/cpu_fixed', cpu_fixed)
app.router.add_get('/health', health)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5002)