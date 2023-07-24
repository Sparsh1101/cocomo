# Cocomo

This is a project made by [Sparsh Gupta](https://github.com/Sparsh1101), [Kevin Joshi](https://github.com/KevinJ-hub), [Kaushal Binjola](https://github.com/KaushalBinjola) & [Hardik Jain](https://github.com/hardikjain1708).  
Database used is PostgreSQL as well and various dependencies like [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/) have been used.  
It is a web app that analysis the estimation accuracy for the time and number of people assigned on the project based on the Cocomo Basic Model.  

## Tech Used

- Python 3.9
- Django
- PostgreSQL
- Bootstrap5

## Running this project  

> **NOTE:** You can also skip the virtual environment steps (1-4)

1. Install virtual env on your system
```bash
pip install virtualenv
```

2. Run the command to create a virtual environment in a folder
```bash
python -m venv {your virtual env name}
```

3. A folder named {your virtual env name} will be created, enter the folder. ( The folder should contain some files and folders created for the virtual environment )

4. Now activate the virtual environment
```bash
Windows- .\Scripts\activate
```

```bash
Macos & Linux- source bin/activate )
```

5. Clone the repository
6. Create the env file using the env-sample file
7. Run the following command from the root of the project, Download "backports.zoneinfo" wheel file from https://www.lfd.uci.edu/~gohlke/pythonlibs/#backports.zoneinfo and run "pip instaall filename.whl"

```bash
pip install -r requirements.txt
```

```bash
py manage.py makemigrations
```

```bash
py manage.py migrate
```

8. Create a super user to access the app

```bash
py manage.py createsuperuser
```

9. Run the server
```bash
py manage.py runserver
```

## Images

![Login Page](screenshots/ss3.png)
---

![Home Page](screenshots/ss1.png)
---

![Results Page](screenshots/ss2.png)
