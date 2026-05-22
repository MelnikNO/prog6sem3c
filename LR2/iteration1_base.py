""" Итерация 1 """

import math
import random
import timeit

def estimate_pi(n_points: int = 100000) -> float:
    """
    Вычисляет приближение числа π методом Монте-Карло.

    Метод основан на генерации случайных точек в квадрате [-1, 1] x [-1, 1]
    и подсчёте доли точек, попавших в единичную окружность.

    n_points : int, optional
        Количество случайных точек для генерации.

    Returns
    float
        Приближённое значение числа π.

    Raises
    ValueError
        Если n_points <= 0.
    """
    if n_points <= 0:
        raise ValueError("n_points must be positive")

    inside = 0

    for i in range(n_points):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x * x + y * y <= 1:
            inside += 1

    return 4.0 * inside / n_points


def benchmark(n_points_list: list = None) -> dict:
    """
    Замер времени выполнения для разного количества точек.

    Parameters
    n_points_list : list, optional
        Список значений n_points для тестирования.
        По умолчанию [10000, 100000, 1000000]

    Returns
    dict
        Словарь {n_points: время_в_секундах}
    """
    if n_points_list is None:
        n_points_list = [10_000, 100_000, 1_000_000]

    results = {}

    print("ИТЕРАЦИЯ 1: ЗАМЕРЫ ПОСЛЕДОВАТЕЛЬНОЙ ВЕРСИИ")

    for n_points in n_points_list:
        random.seed(42)

        stmt = f"estimate_pi({n_points})"
        setup = "from __main__ import estimate_pi; import random; random.seed(42)"

        times = timeit.repeat(stmt, setup=setup, repeat=5, number=3)
        avg_time = sum(times) / len(times)
        results[n_points] = avg_time

        pi_value = estimate_pi(n_points)
        error = abs(pi_value - math.pi)

        print(f"n_points = {n_points:8d} | время = {avg_time:.4f} сек | "
              f"π ≈ {pi_value:.6f} | ошибка = {error:.6f}")

    return results


if __name__ == "__main__":
    print("ПРОВЕРКА DOCTEST:")
    import doctest

    doctest.testmod(verbose=True)

    results = benchmark()

    with open("results.txt", "a") as f:
        f.write("\nИТЕРАЦИЯ 1\n")
        for n_points, t in results.items():
            f.write(f"n_points={n_points}: {t:.4f} сек\n")