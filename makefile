swagger_gen:
	 ./manage.py spectacular --color --file schema.yml

run_app:
	python manage.py runserver