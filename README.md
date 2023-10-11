# EpicEvent

EpicEvent is an event specialized advice and management firm, that supports start-ups willing to organize "epic parties".
This app is a CRM, to monitore all clients and events.

## Installation 

Clone repository
```
git clone https://github.com/Tortique/EpicEvent.git
```

Create a new venv
```
python -m venv env
```

Activate him
```
env\scripts\activate.bat
```

Install all requirements
```
pip install -r requirements.txt
```

Make migrations and migrate
```
python manage.py makemigrations

python manage.py migrate
```

And run server
```
python manage.py runserver
```
