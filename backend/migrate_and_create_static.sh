docker exec infra-backend-1 python manage.py makemigrations
docker exec infra-backend-1 python manage.py migrate
docker exec infra-backend-1 python manage.py collectstatic
docker exec infra-backend-1 cp -r /app/collected_static/. /static/static/
