<!--
.. title: Результаты эксперимента
.. slug: results
.. has_math: true
-->

# Результаты эксперимента

На текущем этапе используются синтетические данные,
имитирующие результаты экспериментов по сравнению методов кэширования.

<div class="row mb-4">

<div class="col-md-6 col-lg-3 mb-4">
<div class="card h-100 shadow-sm">
<div class="card-body">
<p class="text-muted mb-1">Методов</p>
<h3 class="mb-0">5</h3>
</div>
</div>
</div>

<div class="col-md-6 col-lg-3 mb-4">
<div class="card h-100 shadow-sm">
<div class="card-body">
<p class="text-muted mb-1">Запусков</p>
<h3 class="mb-0">15</h3>
</div>
</div>
</div>

<div class="col-md-6 col-lg-3 mb-4">
<div class="card h-100 shadow-sm">
<div class="card-body">
<p class="text-muted mb-1">Средний Hit Rate</p>
<h3 class="mb-0">79.47%</h3>
</div>
</div>
</div>

<div class="col-md-6 col-lg-3 mb-4">
<div class="card h-100 shadow-sm">
<div class="card-body">
<p class="text-muted mb-1">Средняя Latency</p>
<h3 class="mb-0">72.67 ms</h3>
</div>
</div>
</div>

</div>

<div class="alert alert-secondary">
<h5 class="alert-heading">Версия результата</h5>

<p class="mb-1">
<strong>Commit:</strong>
<code>f859873</code>
</p>

<p class="mb-1">
<strong>Dataset version:</strong>
<code>ae42ece19d31</code>
</p>

<p class="mb-0">
<strong>Build time:</strong>
<code>2026-10-02 18:20:14 UTC</code>
</p>
</div>

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

        ## Сводные результаты

        Результаты расчёта исследуемых показателей представлены
        <a href="#table-1">в таблице 1</a>.

        <p class="mb-2"><strong>Таблица 1 — Результаты сравнения методов кэширования</strong></p>
<div id="table-1" class="table-responsive">
<table class="dataframe table table-striped table-hover table-bordered">
  <thead>
    <tr style="text-align: right;">
      <th>method</th>
      <th>runs</th>
      <th>hit_rate</th>
      <th>miss_rate</th>
      <th>latency_ms</th>
      <th>latency_std_ms</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Adaptive</td>
      <td>3</td>
      <td>82.77</td>
      <td>17.23</td>
      <td>68.60</td>
      <td>0.98</td>
    </tr>
    <tr>
      <td>CacheMissPrediction</td>
      <td>3</td>
      <td>81.33</td>
      <td>18.67</td>
      <td>68.40</td>
      <td>0.70</td>
    </tr>
    <tr>
      <td>LFU</td>
      <td>3</td>
      <td>76.17</td>
      <td>23.83</td>
      <td>78.53</td>
      <td>0.75</td>
    </tr>
    <tr>
      <td>LRU</td>
      <td>3</td>
      <td>72.43</td>
      <td>27.57</td>
      <td>84.33</td>
      <td>1.70</td>
    </tr>
    <tr>
      <td>Predictive</td>
      <td>3</td>
      <td>84.67</td>
      <td>15.33</td>
      <td>63.47</td>
      <td>1.23</td>
    </tr>
  </tbody>
</table>
</div>


## Визуализация

Изменение средней доли попаданий в кэш для исследуемых методов
<a href="#fig-hit-rate">представлено на рисунке 1</a>.

<figure id="fig-hit-rate" class="figure d-block text-center">
    <iframe
        src="/plots/hit_rate.html"
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
        src="/plots/latency.html"
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
        src="/images/generated/latency_distribution.png"
        class="figure-img img-fluid"
        alt="Распределение задержки по экспериментальным запускам"
    >

    <figcaption class="figure-caption">
        Рисунок 3 — Распределение задержки по экспериментальным запускам
    </figcaption>
</figure>