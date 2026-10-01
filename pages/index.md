<!--
.. title: Главная
.. slug: index
-->

<div class="jumbotron">
<h1 class="display-4">Cache Research Lab</h1>

<p class="lead">
Демонстрационный исследовательский проект для воспроизводимой обработки,
анализа и публикации результатов экспериментов по кэшированию.
</p>

<hr class="my-4">

<p>
Проект демонстрирует конвейер
<strong>«данные → результат → сайт»</strong>,
в котором результаты эксперимента автоматически преобразуются
в таблицы, графики и опубликованную веб-страницу.
</p>

<a class="btn btn-primary btn-lg" href="/results/" role="button">
Посмотреть результаты
</a>
</div>

## Воспроизводимый конвейер

<div class="row">

<div class="col-md-3 mb-4">
<div class="card h-100">
<div class="card-body">
<h5 class="card-title">1. Данные</h5>
<p class="card-text">
Исходные результаты эксперимента хранятся в структурированном CSV-файле.
</p>
</div>
</div>
</div>

<div class="col-md-3 mb-4">
<div class="card h-100">
<div class="card-body">
<h5 class="card-title">2. Анализ</h5>
<p class="card-text">
Python-скрипт выполняет расчёт метрик и проверяет корректность входных данных.
</p>
</div>
</div>
</div>

<div class="col-md-3 mb-4">
<div class="card h-100">
<div class="card-body">
<h5 class="card-title">3. Результаты</h5>
<p class="card-text">
Автоматически формируются таблицы, статические и интерактивные графики.
</p>
</div>
</div>
</div>

<div class="col-md-3 mb-4">
<div class="card h-100">
<div class="card-body">
<h5 class="card-title">4. Публикация</h5>
<p class="card-text">
Nikola собирает результаты в готовый статический сайт.
</p>
</div>
</div>
</div>

</div>

## Что демонстрирует проект

<div class="row">

<div class="col-md-6 col-lg-3 mb-4">
<div class="card h-100">
<div class="card-body">
<h5 class="card-title">Кэширование</h5>
<p class="card-text">
Неизменившиеся результаты не пересчитываются повторно.
</p>
</div>
</div>
</div>

<div class="col-md-6 col-lg-3 mb-4">
<div class="card h-100">
<div class="card-body">
<h5 class="card-title">Визуализация</h5>
<p class="card-text">
Результаты представлены в виде статических и интерактивных графиков.
</p>
</div>
</div>
</div>

<div class="col-md-6 col-lg-3 mb-4">
<div class="card h-100">
<div class="card-body">
<h5 class="card-title">Научный контент</h5>
<p class="card-text">
Страница поддерживает формулы LaTeX, таблицы и ссылки на рисунки.
</p>
</div>
</div>
</div>

<div class="col-md-6 col-lg-3 mb-4">
<div class="card h-100">
<div class="card-body">
<h5 class="card-title">Версионирование</h5>
<p class="card-text">
Опубликованный результат связан с версией кода и набора данных.
</p>
</div>
</div>
</div>

</div>

## Структура проекта

```text
Данные
   ↓
Python-анализ
   ↓
Таблицы + графики
   ↓
Nikola
   ↓
Статический сайт
```

Все производные материалы формируются автоматически из исходных данных.

## Навигация
Перейдите к странице «Эксперимент», чтобы ознакомиться с описанием
исследуемых данных и методики, или откройте страницу «Результаты»,
где представлены рассчитанные показатели и визуализация.