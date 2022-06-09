# recommender
Рекомендательная система для фильмов

### Установка необходимых пакетов Python 
```bash
pip3 install -r requirements.txt
```

###  Конфигурация Django для подключения к PostGreSql

Откройте `rs_project/settings.py` 

Обновите следующие строки:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'moviegeek',                      
        'USER': 'db_user',
        'PASSWORD': 'db_user_password',
        'HOST': 'db_host',
        'PORT': 'db_port_number',
    }
}
```

### Запуск сервиса БД:
```
sudo service postgresql start
```

### Старт сервера Django
```bash
> python3 manage.py runserver 127.0.0.1:8081
```

### Установка проекта Vue.js

```
npm install
```

### Компиляция и запуск сервера для разработки Vue.js

```
npm run serve
```