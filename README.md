# web app

## purpose

Web app that will scrap web every day and store data in database.

[MPK_Crawler](https://github.com/MIachaI/MPK_Crawler) app will use app service
not to download all information by itself every time (as it takes a *little bit* of time)

## setup

This section describes setting up your working directory.

### repo

Clone remote repository to your hard drive
```
$ git clone https://github.com/umatbro/crawler-helper.git
```

### virtualenv

Setup `virtualenv` for **your own convenience**

[Ref, lasie](https://tutorial.djangogirls.org/pl/django_installation/)

Install `virtualenv`
```
$ sudo apt install virtualenv
```

Create new `virtualenv` by the name of `crawler-env`

```
cd crawler-helper
virtualenv --python=python3.5 crawler-env
```

To start newly created `crawler-env` run following command:

```
$ source crawler-env/bin/activate
```

You can tell that everything is working properly when you console prompt changed to something like this
```
(crawler-env) you@you ~/Documents/crawler-helper $
```

### installing requirements

All dependencies that have to be installed for project to run properly are stored in
`requirements.txt` file.

To install all required dependencies run command:
```
$ pip install -r requirements.txt
```

(ofc you have to be in the catalog with `requirements.txt` file, otherwise it *probably* won't work :sweat:)

## running server locally

easy

```
$ python manage.py runserver
```

After this go to [localhost:8000](http://127.0.0.1:8000) in your browser
You can change default port number with `-p` flag

## running tests

To run tests run command

```
$ python manage.py test
```

To run tests only for specific app, e.g. only for `collector` run
```
$ python manage.py test collector
```


## desired output

Desktop app will ask for link list for given city.

App should return information in **JSON** format.

Example output

```JSON
{
  "Warszawa": {
    "Czerwińska": [
      {
        "512": "http://www.ztm.waw.pl/rozklad_nowy.php?c=182&l=1&a=512&n=1121&o=01"
      },
      {
        "512": "http://www.ztm.waw.pl/rozklad_nowy.php?c=182&l=1&a=512&n=1121&o=02"
      }
    ],
    "Och-Teatr": [
      {
        "167": "http://www.ztm.waw.pl/rozklad_nowy.php?c=182&l=1&a=167&n=4004&o=01"
      },
      {
        "191": "http://www.ztm.waw.pl/rozklad_nowy.php?c=182&l=1&a=191&n=4004&o=01"
      },
      {
        "521": "http://www.ztm.waw.pl/rozklad_nowy.php?c=182&l=1&a=521&n=4004&o=01"
      },
    ]
}

```

This will allow MPK_Crawler app to visit given links and retrieve desired timetables.

**TODO:** revamp JSON structure?