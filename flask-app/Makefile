clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

tests:
	python manage.py test

install:
	pip install -r requirements.txt

run:
	python manage.py run

run-gunicorn:
	gunicorn wsgi:app --reload --workers=1 -b :5000

all: clean install tests db_upgrade run


db_init:
	python manage.py db init

db_migrate:
	python manage.py db migrate --message 'initial database migration'

db_upgrade:
	python manage.py db upgrade

celery-worker-up:
	watchmedo auto-restart --directory . --pattern '*.py' --recursive -- celery worker -A app.main.worker.tasks
