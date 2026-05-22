""" Итерация 5 """

from libc.stdlib cimport rand, RAND_MAX
from cython.parallel import prange
from cython cimport boundscheck, wraparound


cdef double random_nogil() nogil:
    return rand() / <double>RAND_MAX


@boundscheck(False)
@wraparound(False)
def estimate_pi_nogil(int n_points, int n_threads=1):
    """
    Параллельная версия вычисления π с отключённым GIL.

    Parameters
    n_points : int
        Общее количество точек
    n_threads : int
        Количество потоков (2, 4, 6)

    Returns
    float
        Приближённое значение π
    """
    cdef int points_per_thread = n_points // n_threads
    cdef int total_inside = 0
    cdef int i, tid, inside
    cdef double x, y

    for tid in prange(n_threads, nogil=True, num_threads=n_threads):
        inside = 0
        for i in range(points_per_thread):
            x = 2.0 * random_nogil() - 1.0
            y = 2.0 * random_nogil() - 1.0
            if x*x + y*y <= 1.0:
                inside += 1

        total_inside += inside

    return 4.0 * total_inside / n_points


def benchmark_nogil(n_points: int = 10_000_000):
    """
    Сравнение noGIL версии с процессами.
    """
    import timeit

    print("ИТЕРАЦИЯ 5: noGIL vs ПРОЦЕССЫ")
    print(f"Количество точек: {n_points}")

    print("\n noGIL версия (Cython с prange)")
    for n_threads in [2, 4, 6]:
        times = timeit.repeat(
            f"estimate_pi_nogil({n_points}, {n_threads})",
            setup="from iteration5_nogil import estimate_pi_nogil",
            repeat=3,
            number=2
        )
        avg_time = sum(times) / len(times)
        print(f"Потоков = {n_threads}: {avg_time:.4f} сек")

    print("\n--- Процессы (ProcessPoolExecutor) ---")
    from iteration3_processes import estimate_pi_processes
    for n_jobs in [2, 4, 6]:
        times = timeit.repeat(
            f"estimate_pi_processes({n_points}, {n_jobs})",
            setup="from iteration3_processes import estimate_pi_processes",
            repeat=3,
            number=2
        )
        avg_time = sum(times) / len(times)
        print(f"Процессов = {n_jobs}: {avg_time:.4f} сек")
    