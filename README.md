Run those commands in shell:
- docker-compose up -d --build
- docker-compose exec web python3 manage.py createsuperuser
  - Username: admin _(required)_
  - Email: not required
  - Password: required (more than 8 characters, can't be common like 'password123')

Go to: https://localhost:8080

(Delete all containers, images and data:
`docker system prune -a --volumes`)