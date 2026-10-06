from textwrap import dedent
from pathlib import Path

import pandas as pd

from scripts.config import (
    OUTPUT_DIR,
    RESULTS_PAGE,
    ROOT_DIR,
    site_url,
)

from scripts.version import (
    get_build_time,
    get_dataset_version,
    get_git_commit,
)

def build_cards_html(metrics: pd.DataFrame) -> str:
    """Build the summary metric cards."""
    total_methods = len(metrics)
    total_runs = int(metrics["runs"].sum())
    
    total_run_count = metrics["runs"].sum()
    
    average_hit_rate = (
        (metrics["hit_rate"] * metrics["runs"]).sum()
        / total_run_count
    )

    average_latency = (
        (metrics["latency_ms"] * metrics["runs"]).sum()
        / total_run_count
    )
    
    return dedent(
        f"""
        <div class="row mb-4">
        
        <div class="col-md-6 col-lg-3 mb-4">
        <div class="card h-100 shadow-sm">
        <div class="card-body">
        <p class="text-muted mb-1">Методов</p>
        <h3 class="mb-0">{total_methods}</h3>
        </div>
        </div>
        </div>
        
        <div class="col-md-6 col-lg-3 mb-4">
        <div class="card h-100 shadow-sm">
        <div class="card-body">
        <p class="text-muted mb-1">Запусков</p>
        <h3 class="mb-0">{total_runs}</h3>
        </div>
        </div>
        </div>
        
        <div class="col-md-6 col-lg-3 mb-4">
        <div class="card h-100 shadow-sm">
        <div class="card-body">
        <p class="text-muted mb-1">Средний Hit Rate</p>
        <h3 class="mb-0">{average_hit_rate:.2f}%</h3>
        </div>
        </div>
        </div>
        
        <div class="col-md-6 col-lg-3 mb-4">
        <div class="card h-100 shadow-sm">
        <div class="card-body">
        <p class="text-muted mb-1">Средняя Latency</p>
        <h3 class="mb-0">{average_latency:.2f} ms</h3>
        </div>
        </div>
        </div>
        
        </div>
        """
    ).strip()

def build_version_block(
    git_commit: str, 
    dataset_version: str, 
    build_time: str
) -> str:
    """Build the result version metadata block."""
    return dedent(
        f"""
        <div class="alert alert-secondary">
        <h5 class="alert-heading">Версия результата</h5>

        <p class="mb-1">
        <strong>Commit:</strong>
        <code>{git_commit}</code>
        </p>

        <p class="mb-1">
        <strong>Dataset version:</strong>
        <code>{dataset_version}</code>
        </p>

        <p class="mb-0">
        <strong>Build time:</strong>
        <code>{build_time}</code>
        </p>
        </div>
        """
    ).strip()

def build_methodology() -> str:
    """Build the methodology section with LaTeX formulas."""
    return dedent(
        r"""
        ## Методика расчёта

        Для оценки эффективности методов кэширования используются показатели
        доли попаданий в кэш и времени отклика.

        Доля запросов, успешно обработанных из кэша, рассчитывается по
        <a href="#formula-1">формуле (1)</a>:

        <span id="formula-1"></span>

        \\[
        \mathrm{HitRate} =
        \frac{H}{H + M} \times 100\%
        \tag{1}
        \\]

        где

        \\(H\\) — количество попаданий в кэш;

        \\(M\\) — количество промахов.

        Средняя задержка выполнения запросов рассчитывается по
        <a href="#formula-2">формуле (2)</a>:

        <span id="formula-2"></span>

        \\[
        \overline{L} =
        \frac{1}{N}
        \sum_{i=1}^{N} L_i
        \tag{2}
        \\]

        где

        \\(L_i\\) — задержка отдельного запуска;

        \\(N\\) — количество экспериментальных запусков.
        """
    ).strip()

def build_results_table(
    metrics: pd.DataFrame,
) -> str:
    """Build the results table with Bootstrap styling."""
    table_html = metrics.to_html(
        index=False,
        classes=[
            "table",
            "table-striped",
            "table-hover",
            "table-bordered",
        ],
        border=0,
    )

    return (
        '<p class="mb-2"><strong>'
        "Таблица 1 — Результаты сравнения методов кэширования"
        "</strong></p>\n"
        '<div id="table-1" class="table-responsive">\n'
        f"{table_html}\n"
        "</div>"
    )


def build_visualizations() -> str:
    """Build the visualization section."""
    hit_rate_url = site_url(
        "plots/hit_rate.html"
    )

    latency_url = site_url(
        "plots/latency.html"
    )

    latency_distribution_url = site_url(
        "images/generated/latency_distribution.png"
    )

    return dedent(
        f"""
        ## Визуализация

        Изменение средней доли попаданий в кэш для исследуемых методов
        <a href="#fig-hit-rate">представлено на рисунке 1</a>.

        <figure id="fig-hit-rate" class="figure d-block text-center">
            <iframe
                src="{hit_rate_url}"
                width="100%"
                height="500"
                frameborder="0"
                loading="lazy">
            </iframe>

            <figcaption class="figure-caption">
                Рисунок 1 — Сравнение средней доли попаданий в кэш
            </figcaption>
        </figure>

        Средняя задержка ответа для исследуемых методов
        <a href="#fig-latency">представлена на рисунке 2</a>.

        <figure id="fig-latency" class="figure d-block text-center">
            <iframe
                src="{latency_url}"
                width="100%"
                height="500"
                frameborder="0"
                loading="lazy">
            </iframe>

            <figcaption class="figure-caption">
                Рисунок 2 — Сравнение средней задержки ответа
            </figcaption>
        </figure>

        Распределение значений задержки между отдельными экспериментальными
        запусками
        <a href="#fig-latency-distribution">
        представлено на рисунке 3
        </a>.

        <figure
            id="fig-latency-distribution"
            class="figure d-block text-center"
        >
            <img
                src="{latency_distribution_url}"
                class="figure-img img-fluid"
                alt="Распределение задержки по экспериментальным запускам"
            >

            <figcaption class="figure-caption">
                Рисунок 3 — Распределение задержки по экспериментальным запускам
            </figcaption>
        </figure>
        """
    ).strip()


def generate_report(metrics: pd.DataFrame) -> Path:
    """Generate the complete experiment report."""
    output_file = OUTPUT_DIR / "results.md"

    git_commit = get_git_commit(ROOT_DIR)
    dataset_version = get_dataset_version(
        ROOT_DIR / "data" / "experiment_results.csv"
    )
    build_time = get_build_time()

    cards_html = build_cards_html(metrics)

    version_block = build_version_block(
        git_commit,
        dataset_version,
        build_time,
    )

    methodology = build_methodology()
    results_table = build_results_table(metrics)
    visualizations = build_visualizations()

    markdown = dedent(
        f"""
        <!--
        .. title: Результаты эксперимента
        .. slug: results
        .. has_math: true
        -->

        На текущем этапе используются синтетические данные,
        имитирующие результаты экспериментов по сравнению методов кэширования.
        """
    ).strip()

    markdown += "\n\n" + cards_html
    markdown += "\n\n" + version_block
    markdown += "\n\n" + methodology

    markdown += f"""\n
## Сводные результаты

Результаты расчёта исследуемых показателей представлены
<a href="#table-1">в таблице 1</a>.

{results_table}
        """

    markdown += "\n\n" + visualizations

    output_file.write_text(
        markdown,
        encoding="utf-8",
    )

    RESULTS_PAGE.write_text(
        markdown,
        encoding="utf-8",
    )

    return output_file