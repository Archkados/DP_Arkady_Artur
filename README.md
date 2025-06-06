# CRM система — веб-приложение

## Обзор

Данный репозиторий содержит веб-приложение CRM (Customer Relationship Management), основанное на фреймворке Django. Система предназначена для управления логистическими процессами, с акцентом на обработку виз и отслеживание заявок для логистических компаний.

## Используемые технологии

* **Бэкенд:** Python 3.x
* **Фреймворк:** Django
* **База данных:** SQLite (стандартная база данных Django)

## Структура проекта

Проект следует стандартной структуре Django:

* **manage.py:** утилита командной строки Django для административных задач.
* **crm\_system:** главная директория проекта.
* **visas:** Django-приложение, отвечающее за бизнес-логику, взаимодействие с пользователями и модели данных.

### Основные файлы:

* `models.py`: содержит определения схем базы данных с использованием Django ORM.
* `views.py`: реализует бизнес-логику и обработку HTTP-запросов.
* `forms.py`: управляет созданием и валидацией форм.
* `urls.py`: задаёт URL-маршруты для обработки запросов.
* `admin.py`: конфигурация административной панели Django для управления данными.

### Дополнительные функции

* **Пользовательские шаблонные теги:** расположены в `templatetags/group_tags.py`.
* **Шаблоны:** HTML-шаблоны, динамически генерируемые представлениями Django.

## Установка

Для запуска проекта локально:

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Archkados/DP_Arkady_Artur.git
```

2. Перейдите в директорию проекта:

```bash
cd crm_system
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Примените миграции:

```bash
python manage.py migrate
```

5. Запустите сервер разработки:

```bash
python manage.py runserver
```

Откройте браузер и перейдите по адресу: `http://localhost:8000`.

## База данных

Проект использует SQLite по умолчанию, подходящую для разработки и тестирования.

## Архитектура

Проект построен на архитектуре Model-View-Template (MVT) Django:

* **Модели:** описывают схемы базы данных.
* **Представления (views):** обрабатывают запросы, взаимодействуют с моделями и передают данные в шаблоны.
* **Шаблоны:** генерируют динамический HTML-код.

## Вклад в проект

Приветствуются любые улучшения и доработки. Форкните репозиторий и отправьте pull request.

---

Разработчики: Аркадий Величковский и Артур Бабич
