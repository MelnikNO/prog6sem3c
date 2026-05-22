""" Итерация 2 """

import random
import timeit
import concurrent.futures as ftres

def estimate_pi_chunk(n_points: int, seed: int = None) -> float:
    """
    Вычисляет π для параллельной версии.

    Parameters
    n_points : int
    seed : int, optional
        Seed для генератора случайных чисел

    Returns
    float
        Приближённое значение π
    """
    if seed is not None:
        random.seed(seed)

    inside = 0
    for i in range(n_points):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x * x + y * y <= 1:
            inside += 1

    return 4.0 * inside / n_points


def estimate_pi_threads(n_points: int = 100000, n_jobs: int = 2) -> float:
    """
    Параллельное вычисление π с использованием потоков.

    Parameters
    n_points : int
        Общее количество точек
    n_jobs : int
        Количество потоков (2, 4, 6, 8)

    Returns
    float
        Приближённое значение π
    """
    points_per_job = n_points // n_jobs

    with ftres.ThreadPoolExecutor(max_workers=n_jobs) as executor:
        futures = []
        for i in range(n_jobs):
            seed = i * 1000
            future = executor.submit(estimate_pi_chunk, points_per_job, seed)
            futures.append(future)

        results = [f.result() for f in ftres.as_completed(futures)]

    return sum(results) / n_jobs


def benchmark_threads(n_points: int = 1_000_000):
    """
    Parameters
    n_points : int
        Общее количество точек для тестирования
    """
    print("ИТЕРАЦИЯ 2: Потоки")
    print(f"Общее количество точек: {n_points}")

    seq_time = timeit.timeit(
        f"estimate_pi({n_points})",
        setup="from iteration1_base import estimate_pi; import random; random.seed(42)",
        number=3
    )
    print(f"Последовательно: {seq_time:.4f} сек (1 поток)")

    results = {}

    for n_jobs in [2, 4, 6, 8]:
        times = timeit.repeat(
            f"estimate_pi_threads({n_points}, {n_jobs})",
            setup="from __main__ import estimate_pi_threads; import random",
            repeat=3,
            number=3
        )
        avg_time = sum(times) / len(times)
        results[n_jobs] = avg_time

        print(f"Потоков = {n_jobs}: {avg_time:.4f} сек | "
              f"отношение к последовательной = {avg_time / seq_time:.2f}x")

    print("\n")

    return results


if __name__ == "__main__":
    results = benchmark_threads()

    with open("results.txt", "a") as f:
        f.write("\nИТЕРАЦИЯ 2 (ПОТОКИ)\n")
        f.write("Из-за GIL ускорение отсутствует\n")
        for n_jobs, t in results.items():
            f.write(f"n_jobs={n_jobs}: {t:.4f} сек\n")