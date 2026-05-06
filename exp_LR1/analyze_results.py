import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
from pathlib import Path

def load_stats_from_csv(csv_path: str) -> dict:
    """
    Загружает статистику из stats_history.csv, сгенерированного Locust.
    Возвращает словарь с медианными значениями метрик.
    """
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return None

    df = pd.read_csv(csv_path)

    # Статистика по всем эндпоинтам (усредняем по временным срезам)
    stats = {
        'avg_rps': df['Requests/s'].mean() if 'Requests/s' in df.columns else 0,
        'avg_latency': df['Average response time'].mean() if 'Average response time' in df.columns else 0,
        'p95': df['95%'].mean() if '95%' in df.columns else 0,
        'p99': df['99%'].mean() if '99%' in df.columns else 0,
        'error_rate': (df['Failure count'].sum() / (df['Request count'].sum() + 1)) * 100 if 'Failure count' in df.columns else 0
    }
    return stats


def find_all_results(results_dir: str = "reports") -> dict:
    """Автоматически находит все CSV-файлы в папке reports"""
    results = {}
    csv_files = glob.glob(os.path.join(results_dir, "*_stats_history.csv"))

    for filepath in csv_files:
        filename = os.path.basename(filepath)
        parts = filename.replace('_stats_history.csv', '').split('_')
        if len(parts) >= 3:
            framework = parts[0]
            users = parts[1]
            endpoint = '_'.join(parts[2:]) if len(parts) > 3 else parts[2]
            key = f"{framework}_{users}_{endpoint}"
            results[key] = load_stats_from_csv(filepath)

    return results


def create_comparison_plots(results: dict):
    """Создает сводные графики для всех тестов"""
    frameworks = ['flask', 'tornado']
    endpoints = ['cpu', 'cpu_fixed']
    user_counts = [50, 100, 200]
    metrics = ['avg_rps', 'avg_latency', 'p95', 'p99', 'error_rate']

    rows = []
    for key, stats in results.items():
        if stats is None:
            continue
        parts = key.split('_')
        if len(parts) >= 3:
            framework = parts[0]
            users = parts[1]
            endpoint = '_'.join(parts[2:])
            row = {'framework': framework, 'users': int(users), 'endpoint': endpoint}
            row.update(stats)
            rows.append(row)

    df = pd.DataFrame(rows)

    if df.empty:
        print("No data found!")
        return

    # График 1: RPS (Requests Per Second)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    for idx, metric in enumerate(['avg_rps', 'avg_latency', 'p95', 'error_rate']):
        ax = axes[idx // 2, idx % 2]

        for endpoint in endpoints:
            for framework in frameworks:
                subset = df[(df['endpoint'] == endpoint) & (df['framework'] == framework)]
                if not subset.empty:
                    subset_sorted = subset.sort_values('users')
                    ax.plot(subset_sorted['users'], subset_sorted[metric],
                            marker='o', label=f"{framework} / {endpoint}")

        ax.set_xlabel('Number of concurrent users')
        metric_names = {
            'avg_rps': 'RPS (Requests/sec)',
            'avg_latency': 'Avg Latency (ms)',
            'p95': 'P95 Latency (ms)',
            'error_rate': 'Error Rate (%)'
        }
        ax.set_ylabel(metric_names.get(metric, metric))
        ax.set_title(f'{metric_names.get(metric, metric)} comparison')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('reports/comparison_plot.png', dpi=150)
    plt.show()

    print("\n" + "=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    summary_table = df.pivot_table(
        index=['framework', 'endpoint', 'users'],
        values=['avg_rps', 'avg_latency', 'p95', 'error_rate']
    ).round(2)
    print(summary_table)

    df.to_csv('reports/summary.csv', index=False)
    print("\nSummary saved to reports/summary.csv")


if __name__ == "__main__":
    Path("reports").mkdir(exist_ok=True)

    results = find_all_results()

    if not results:
        print("No CSV files found in 'reports/' directory.")
        print("Creating sample data for demonstration...")

        sample_data = {
            'flask_50_cpu': {'avg_rps': 45, 'avg_latency': 1100, 'p95': 1500, 'p99': 2000, 'error_rate': 0.1},
            'flask_100_cpu': {'avg_rps': 48, 'avg_latency': 2100, 'p95': 2800, 'p99': 3500, 'error_rate': 0.3},
            'flask_200_cpu': {'avg_rps': 49, 'avg_latency': 4100, 'p95': 5500, 'p99': 7000, 'error_rate': 1.2},
            'sanic_50_cpu': {'avg_rps': 120, 'avg_latency': 400, 'p95': 550, 'p99': 700, 'error_rate': 0},
            'sanic_100_cpu': {'avg_rps': 125, 'avg_latency': 780, 'p95': 1050, 'p99': 1300, 'error_rate': 0},
            'sanic_200_cpu': {'avg_rps': 118, 'avg_latency': 1650, 'p95': 2200, 'p99': 2800, 'error_rate': 0.5},
            'sanic_50_cpu_fixed': {'avg_rps': 450, 'avg_latency': 105, 'p95': 150, 'p99': 180, 'error_rate': 0},
            'sanic_100_cpu_fixed': {'avg_rps': 890, 'avg_latency': 110, 'p95': 160, 'p99': 195, 'error_rate': 0},
            'sanic_200_cpu_fixed': {'avg_rps': 1720, 'avg_latency': 115, 'p95': 170, 'p99': 210, 'error_rate': 0},
            'tornado_50_cpu': {'avg_rps': 95, 'avg_latency': 520, 'p95': 700, 'p99': 900, 'error_rate': 0},
            'tornado_100_cpu': {'avg_rps': 98, 'avg_latency': 1020, 'p95': 1350, 'p99': 1700, 'error_rate': 0},
            'tornado_200_cpu': {'avg_rps': 92, 'avg_latency': 2150, 'p95': 2900, 'p99': 3600, 'error_rate': 0.2},
            'tornado_50_cpu_fixed': {'avg_rps': 520, 'avg_latency': 92, 'p95': 130, 'p99': 155, 'error_rate': 0},
            'tornado_100_cpu_fixed': {'avg_rps': 980, 'avg_latency': 98, 'p95': 140, 'p99': 170, 'error_rate': 0},
            'tornado_200_cpu_fixed': {'avg_rps': 1890, 'avg_latency': 105, 'p95': 155, 'p99': 190, 'error_rate': 0},
        }
        results = sample_data

    create_comparison_plots(results)