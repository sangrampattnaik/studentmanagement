manage=./manage.py
python=python

runserver:
	@$(python) $(manage) runserver

initial-setup: 

	@$(python) $(manage) makemigrations
	@$(python) $(manage) migrate
	@$(python) $(manage) initial_setup

superuser:
	@$(python) $(manage) superadmin

migrate:
	@$(python) $(manage) makemigrations
	@$(python) $(manage) migrate
