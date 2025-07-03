# Clinic Appointments
Микросервис для записи пациентов к врачу с REST API, реализованный на FastAPI и PostgreSQL.

## Быстрый старт
```bash
git clone <repo_url>
cd clinic_appointments
```

## Создайте файл окружения

```bash
cp .env.example .env
```

## Запустите сервисы

```bash
docker compose up -d --build

#или команда Make
make up
```

## Основные команды

    make help - помощь (эта справка о доступных командах)
    make lint — проверка стиля c помощью ruff (заменяет black, isort, flake8)
    make test — запуск тестов
    make up — запуск сервисов
    make down — остановка сервисов

## Документация

    Архитектурная схема: diagrams/architecture.png
    ER-диаграмма: diagrams/er_diagram.png
    Activity-диаграмма: diagrams/activity_diagram.png
    Бизнес-процесс: diagrams/business_logic.png
    Bot-сценарий: docs/bot_scenario.md
    Проектирование → реализация: docs/design_to_implementation.md
    Опрос: answers.txt

## Бонус: строгая типизация mypy

- Покрытие типами mypy: 90%+
- Проверено командой:
```bash
  mypy src/ --html-report htmlmypy
```
- В отчёте htmlmypy/index.html:  
  Total 9.88% imprecise, 962 LOC (т.е. покрытие 90.12%)

## Бонус: Kubernetes-манифест для деплоя

Приложение можно развернуть в Kubernetes:

```bash
kubectl apply -f k8s/

kubectl port-forward svc/clinic-app 8000:8000
```

## Бонус: CI собирает и пушит Docker-образ

Реализована сборка Docker-образа с помощью GitHub Actions и пуш в мой репозиторий на DockerHub.
