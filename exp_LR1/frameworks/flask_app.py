from flask import Flask, jsonify, request
import time
import os

app = Flask(__name__)

def cpu_intensive_task(iterations: int = 15_000_000) -> float:
    total = 0
    for i in range(iterations):
        total += i
    return total

@app.route('/cpu', methods=['GET'])
def cpu_bound():
    iterations = int(request.args.get('n', 15_000_000))
    start = time.time()
    result = cpu_intensive_task(iterations)
    elapsed = time.time() - start
    return jsonify({
        'result': result,
        'time_seconds': elapsed,
        'iterations': iterations,
        'mode': 'blocking'
    })

@app.route('/cpu_fixed', methods=['GET'])
def cpu_fixed():
    """Для синхронного Flask неблокирующего режима нет"""
    iterations = 15_000_000
    start = time.time()
    result = cpu_intensive_task(iterations)
    elapsed = time.time() - start
    return jsonify({
        'result': result,
        'time_seconds': elapsed,
        'iterations': iterations,
        'mode': 'blocking (синхронный фреймворк не поддерживает async)'
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=False, processes=1)