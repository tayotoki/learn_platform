## Создать файл ```.env```

    SSECRET_KEY="django-insecure-&lz)l^-n14_aj3!4@(p)#e7r$z1ze18^b$-w90ny@jx(#+3a!("

    # POSTGRESQL
    DB_NAME=courses
    DB_USER=postgres
    DB_PASSWORD=12345
    DB_HOST=localhost
    DB_PORT=5432
    
    # SWAGGER_UI
    API_DOCS_ENABLE=True
    
    # STRIPE
    STRIPE_API_KEY=sk_test_51OrDzYJHaROG4J4k6q3hNwudW7FSoTjNhPKSdg2dXoHXcZkfA8WzCTLeLO5isKMucOSydvF6lJGf04J4nPKyLirv00aRrsxAPb

## Наполнение базы данных из фикстуры

    python manage.py loaddata data_dump.json

## Наполнение базы данных из sql-скрипта (pg_dump)

    python manage.py load_data

## Данные суперпользователя для проверки эндпоинтов

    email: "root@root.com"
    password: "1234"

Подключена JWT авторизация, поэтому необходимо получить токены по этим данным и передавать в headers access токен, например:

    curl -X 'GET' \
      'http://0.0.0.0:8000/api/courses/1/' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIi...'