# Лабораторная работа: Методы оптимизации вычисления кода с помощью потоков, процессов, Cython, отпускания GIL

**Цель работы:** исследовать методы оптимизации вычисления кода, используя потоки, процессы, Cython и отключение GIL на примере задачи вычисления числа π методом Монте-Карло.

### Необходимо реализовать 5 итераций:

1. **Базовая реализация**
   - Написать функцию `estimate_pi(n_points)`
   - Добавить полный docstring (PEP 257)
   - Использовать аннотации типов (PEP 484)
   - Включить примеры в docstring для doctest
   - Написать юнит-тесты (unittest/pytest)
   - Провести замеры времени выполнения для разных `n_points`

2. **Оптимизация с помощью потоков (`ThreadPoolExecutor`)**
   - Реализовать функцию `estimate_pi_threads(n_points, n_jobs)`
   - Замерить время для 2, 4, 6, 8 потоков
   - Сделать вывод о влиянии GIL на производительность

3. **Оптимизация с помощью процессов (`ProcessPoolExecutor`)**
   - Реализовать функцию `estimate_pi_processes(n_points, n_jobs)`
   - Замерить время для 2, 4, 6, 8 процессов
   - Вычислить ускорение относительно последовательной версии

4. **Оптимизация с помощью Cython**
   - Переписать функцию `estimate_pi` в Cython с аннотациями типов
   - Сгенерировать HTML-отчет (`cython -a`)
   - Сравнить производительность с чистой Python-версией

5. **noGIL-параллелизм с OpenMP**
   - Реализовать `estimate_pi_nogil` с использованием `prange` и отключением GIL
   - Использовать C-функцию `rand()` для генерации случайных чисел
   - Замерить время для 2, 4, 6 потоков
   - Сравнить с многопроцессной версией

---

## Выполнение работы

### Итерация 1: Базовая реализация

**Файл:** `iteration1_base.py`

Реализована функция `estimate_pi(n_points: int) -> float` с:
- Полным docstring в формате PEP 257
- Аннотациями типов
- Проверкой входных данных (`n_points > 0`)
- Встроенными примерами для doctest

<img width="894" height="453" alt="image" src="https://github.com/user-attachments/assets/88164e9c-e281-4079-8d3a-ad3a18a82226" />

---

### Итерация 2: Многопоточность (Threads)

**Файл:** `iteration2_threads.py`

Реализована функция `estimate_pi_threads(n_points, n_jobs)`, которая делит общее количество точек между потоками и собирает результаты.

**Результаты замеров (`results.txt`):**

| Потоков | Время (сек) | Ускорение |
|---------|-------------|-----------|
| 1 (посл.) | 1.7220 | 1.00x |
| 2 | 1.8671 | 0.92x |
| 4 | 1.5164 | 1.14x |
| 6 | 1.4292 | 1.20x |
| 8 | 1.4324 | 1.20x |

**Вывод:** Из-за GIL (Global Interpreter Lock) потоки не дают реального ускорения. Время выполнения не уменьшается пропорционально количеству потоков из-за накладных расходов на синхронизацию.

<img width="736" height="393" alt="image" src="https://github.com/user-attachments/assets/bf2cf333-63ae-4b9a-b972-429a21a39ee7" />


---

### Итерация 3: Многопроцессность (Processes)

**Файл:** `iteration3_processes.py`

Реализована функция `estimate_pi_processes(n_points, n_jobs)` с использованием `ProcessPoolExecutor`. В отличие от потоков, процессы обходят GIL и дают реальное ускорение.

**Результаты замеров (`results.txt`):**

| Процессов | Время (сек) | Ускорение |
|-----------|-------------|-----------|
| 1 (посл.) | 1.7220 | 1.00x |
| 2 | 1.5100 | 1.14x |
| 4 | 1.0060 | 1.71x |
| 6 | 0.7758 | 2.22x |
| 8 | 0.8186 | 2.10x |

**Вывод:** Процессы дают реальное ускорение за счёт обхода GIL. Оптимальное количество процессов — 6 (соответствует количеству ядер/потоков процессора). Дальнейшее увеличение числа процессов не улучшает производительность из-за накладных расходов на межпроцессное взаимодействие.

<img width="758" height="439" alt="image" src="https://github.com/user-attachments/assets/0316e983-8ba0-4152-b90f-d21395b2330a" />


---

### Итерация 4: Cython

**Файл:** `iteration4_cython.pyx`

Cython-версия функции с аннотациями типов C (`cdef int`, `cdef double`). Это позволяет компилировать критический цикл в нативный C-код.

**Сгенерированный файлы:** 

- [iteration4_cython](https://github.com/MelnikNO/prog6sem3c/blob/main/LR2/iteration4_cython.c)
- [iteration4_cython.cp312-win_amd64](https://github.com/MelnikNO/prog6sem3c/blob/main/LR2/iteration4_cython.cp312-win_amd64.pyd)
- [iteration4_cython](https://github.com/MelnikNO/prog6sem3c/blob/main/LR2/iteration4_cython.html)
- [iteration4_cython.pyx](https://github.com/MelnikNO/prog6sem3c/blob/main/LR2/iteration4_cython.pyx)

---

### Итерация 5: noGIL-параллелизм с OpenMP

**Файл:** `iteration5_nogil.pyx`

Ключевые особенности:
- Использование `from cython.parallel import prange`
- Собственная C-функция `random_nogil()` на базе `rand()`
- Отключение GIL (`nogil=True`)
- Автоматическая редукция результатов (`total_inside += inside`)

**Сгенерированный файлы:** 

- [iteration5_nogil](https://github.com/MelnikNO/prog6sem3c/blob/main/LR2/iteration5_nogil.c)
- [iteration5_nogil.cp312-win_amd64](https://github.com/MelnikNO/prog6sem3c/blob/main/LR2/iteration5_nogil.cp312-win_amd64.pyd)
- [iteration5_nogil](https://github.com/MelnikNO/prog6sem3c/blob/main/LR2/iteration5_nogil.html)
- [iteration5_nogil](https://github.com/MelnikNO/prog6sem3c/blob/main/LR2/iteration5_nogil.pyx)

---

### Юнит-тестирование

**Файл:** `test_pi.py`

<img width="1440" height="329" alt="image" src="https://github.com/user-attachments/assets/43020d5b-46f4-453e-888e-83d8ed46acfb" />

