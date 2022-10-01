# Aviate

## Create a .env file to store environment variables
## Format of .env:
### SECRET_KEY=''
### DEBUG=
### JWT_ALGORITHM=''
### JWT_EXPIRY_IN_SEC=

## To run the server, follow the below steps
1. Better to create virtual environment and then activate it.
2. pip install -r requirements.txt
3. python manage.py makemigrations
4. python manage.py migrate
5. python manage.py runserver
