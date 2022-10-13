# Cocomo

This is a project made by [Kevin Joshi](https://github.com/KevinJ-hub), [Kaushal Binjola](https://github.com/KaushalBinjola), [Sparsh Gupta](https://github.com/Sparsh1101) & [Hardik Jain](https://github.com/hardikjain1708).  
Database used is PostgreSQL as well and various dependencies like [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/) have been used.  
It is a web app that analysis the estimation accuracy for the time and number of people assigned on the project based on the Cocomo Basic Model.  

## Tech Used

- Python
- Django
- PostgreSQL
- Bootstrap5

## Running this project  

1. Clone the repository
2. Create the env file using the env-sample file
3. Run the following command from the root of the project

```bash
pip install -r requirements.txt
```

```bash
py manage.py makemigrations
```

```bash
py manage.py migrate
```

4. Create a super user to access the app

```bash
py manage.py createsuperuser
```

5. Run the server

```bash
py manage.py runserver
```

> **NOTE:** You can also create a virtual environment, activate it and follow the above steps.

## Images

![Login Page](screenshots/ss3.png)
---

![Home Page](screenshots/ss1.png)
---

![Results Page](screenshots/ss2.png)
