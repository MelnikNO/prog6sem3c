""" Итерация 3 """

import timeit
import concurrent.futures as ftres
from iteration2_threads import estimate_pi_chunk


def estimate_pi_processes(n_points: int = 100000, n_jobs: int = 2) -> float:
    """
    Параллельное вычисление π с использованием процессов.

    Parameters
    n_points : int
        Общее количество точек
    n_jobs : int
        Количество процессов (2, 4, 6, 8)

    Returns
    float
        Приближённое значение π
    """
    points_per_job = n_points // n_jobs

    with ftres.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        futures = []
        for i in range(n_jobs):
            seed = i * 1000
            future = executor.submit(estimate_pi_chunk, points_per_job, seed)
            futures.append(future)

        results = [f.result() for f in ftres.as_completed(futures)]

    return sum(results) / n_jobs


def benchmark_processes(n_points: int = 1_000_000):
    """
    Замер времени для процессов с разным количеством воркеров.
    """
    print("ИТЕРАЦИЯ 3: Процессы (ProcessPoolExecutor)")
    print(f"Общее количество точек: {n_points}")
    print("=" * 60)

    seq_time = timeit.timeit(
        f"estimate_pi({n_points})",
        setup="from iteration1_base import estimate_pi; import random; random.seed(42)",
        number=3
    )
    print(f"Последовательно: {seq_time:.4f} сек")

    results = {}

    for n_jobs in [2, 4, 6, 8]:
        times = timeit.repeat(
            f"estimate_pi_processes({n_points}, {n_jobs})",
            setup="from __main__ import estimate_pi_processes",
            repeat=3,
            number=3
        )
        avg_time = sum(times) / len(times)
        speedup = seq_time / avg_time
        results[n_jobs] = (avg_time, speedup)

        print(f"Процессов = {n_jobs}: {avg_time:.4f} сек | "
              f"ускорение = {speedup:.2f}x")

    print("\n")
    print("Вывод: Процессы дают реальное ускорение за счёт обхода GIL")
    print(f"Максимальное ускорение: ~{max(s[1] for s in results.values()):.2f}x")

    return results


if __name__ == "__main__":
    results = benchmark_processes()

    with open("results.txt", "a") as f:
        f.write("\nИТЕРАЦИЯ 3 (ПРОЦЕССЫ)\n")
        for n_jobs, (t, speedup) in results.items():
            f.write(f"n_jobs={n_jobs}: {t:.4f} сек, ускорение={speedup:.2f}x\n")
