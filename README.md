# Parser на Scrapy

python 3.6

## Установка

```bash
# Устанавливаем и запускаем виртуальное окружение
python3 -m venv .env
source .env/bin/activate
# Инсталируем зависимости
pip install -r requirements.txt
```

## Настройки

В файле custom_settings.py должны храниться настройки необходимые для работы парсера

- ALLOWED_DOMAINS = ['site.com']
- START_URLS = ['<https://site.com/users/index>']
- USER_LOGIN = 'login'
- USER_PASSWORD = 'password'

## Запуск

```bash
# Запускаем из папки соответствующего парсера. Например из папки report
cd report
scrapy crawl report
# Собранные данные будут в файле report.csv
```
