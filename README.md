# Python-Webscraping-Project
### [Jakub Barber](https://github.com/BARBUR02)
### [Marek Żuwała](https://github.com/marek-02)

## About project
Project written entirely in Django allows you to scrape data from popular tutoring sites, view and filter them. The application also gives you the opportunity of creating a new account, logging in, adding your own offer, editing it or viewing statistics related to it.

Project made for a Python course at AGH.

## Configuration
```console
git clone https://github.com/BARBUR02/Python-Webscraping-Project
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r .\requirements.txt
cd .\WebScraping\
```
create .env file with your own SECRET_KEY (in WebScraping folder)
```console
py manage.py makemigrations
py manage.py migrate
py manage.py crawl
py manage.py runserver
```
