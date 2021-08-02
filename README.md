# Taiga MIEM Middleware

Taiga MIEM Middleware - это новое, более гибкое и мощное решение задачи удовлетворения требований MIEM ведения проектной деятельности в сервисе Taiga.

## Зачем это понадобилось?

Новое решение теперь является непосредственно частью сервиса (плагин), что улучшает их взаимодействие, ускоряет разработку и упрощает установку.

## Что оно делает?
Был разработан новый API, который позволяет интегрироваться с сервисом Taiga определенным способом, а именно: 
- Создание проектов для трекинга
- Добавление пользователей в эти проекты с определенными правами (лидер/участник) и ролью
- Учет тредозатрат `(TODO)`
- еще больше фич...

## Установка
После установки Taiga и клонирования этого репозитория:
```bash
cd taiga-miem-middleware
workon taiga
pip install -e .
```

В настройках Taiga:
```python
INSTALLED_APPS += ["taiga_miem_middleware"]
```

Обязательно после этого нужно сделать мигрирование в Django:
```bash
DJANGO_SETTINGS_MODULE=settings.your_settings python3 manage.py makemigrations taiga_miem_middleware
DJANGO_SETTINGS_MODULE=settings.your_settings python3 manage.py migrate taiga_miem_middleware
```