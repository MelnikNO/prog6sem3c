""" Итерация 4 """

import random


def estimate_pi_cython(int n_points):
    """
    Cython-версия вычисления π методом Монте-Карло.

    Parameters
    n_points : int
        Количество случайных точек

    Returns
    float
        Приближённое значение π
    """
    cdef int inside = 0
    cdef double x, y
    cdef int i

    for i in range(n_points):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x*x + y*y <= 1:
            inside += 1

    return 4.0 * inside / n_points


def benchmark_cython(n_points: int = 1_000_000):
    """
    Сравнение производительности Cython и чистого Python.
    """
    import timeit

    print("ИТЕРАЦИЯ 4: CYTНON vs ЧИСТЫЙ PYTHON")
    print(f"Количество точек: {n_points}")

    py_time = timeit.timeit(
        f"estimate_pi({n_points})",
        setup="from iteration1_base import estimate_pi; import random; random.seed(42)",
        number=3
    )
    print(f"Чистый Python: {py_time:.4f} сек")

    cy_time = timeit.timeit(
        f"estimate_pi_cython({n_points})",
        setup="from iteration4_cython import estimate_pi_cython; import random; random.seed(42)",
        number=3
    )
    print(f"Cython: {cy_time:.4f} сек")
    print(f"Ускорение: {py_time/cy_time:.2f}x")
