manage=./manage.py
python=python

runserver:
	# run development server
	@$(python) $(manage) runserver

initial-setup: 
	# create database and table
	# create super user of username = admin and password = admin

	@$(python) $(manage) makemigrations
	@$(python) $(manage) migrate
	@$(python) $(manage) initial_setup

superuser:
	# create superuser
	@$(python) $(manage) superadmin

migrate:
	# create database and table
	@$(python) $manage) makemigrations
	@$(python) $(manage) migrate
