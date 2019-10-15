- docker build .
- docker-compose run web python /code/manage.py migrate --noinput
- docker-compose up -d --build

Go to: https://localhost:8080
