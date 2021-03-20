# Student  Management System

 Note - 1: Postgres database should be installed. configure postgres credential and connection by creating .env file by following .env.example file.
 
 Note - 2: Don' t create superuser by `python manage.py createsuperuser`. Use `make superuser` or `python manage.py superadmin`. 


## step - 1
clone the project <br >
` git clone https://github.com/sangrampattnaik/studentmanagement.git`


## step - 2
create a virtual environment with name venv and activate <br >
`virtualenv venv` <br >
`source venv/bib/activate`


## step - 3
install depedancies <br >
`pip install -r requirements.txt`


## step - 4
create databases <br >
`make migrate` <br >
or <br >

`python manage.py makemigrations`
`python manage.py migrate`

## step - 5
initial set up <br >
`make intial-setup` <br >
or <br >
`python manage.py initial_setup`

## step - 6
create admin <br >
`make superuser` <br >
or <br >
`python manage.py superadmin`

## step - 7
runserver <br >
`make runserver` <br >
or <br >
`python manage.py runserver`

## step - 8
swagger documentaion <br >
`http://127.0.0.1:8000/swagger/`

# How To use API
## after creating super admin follow the swagger documentaion 
