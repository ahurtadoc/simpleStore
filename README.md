## Simple Django Store

---

The project is a simple web store that use Placetopay payment gateway to create orders of one product and emulate states that could be taken according to payment result. It is built in python with Django framework 

### Installation
Require: 
- Python >= 3.8
- Django = 3.1.7
- httpx

Install python for your OS directly from official web page
https://www.python.org/

To install django and httpx it is needed pip installed and configured. For more information see https://pip.pypa.io/en/stable/installing/

After python and pip work correctly, install in you system the framework and library with the next commands
```
python -m pip install Django
```
for Windows
```
py -m pip install Django
```
 and the library to make http request
 ```
 pip install httpx
 ```
for more information about these installations see: 

https://www.python-httpx.org/
https://docs.djangoproject.com/en/3.1/topics/install/

### Use

With django installed and configured, in your project path can run the *manage.py* file with the specific commands to config database:
```
python manage.py makemigrations
```
After that, the project is ready to work in it (See Django [documentation](https://docs.djangoproject.com/en/3.1/contents/)).

To see the application, run the command 
```
python manage.py runserver
```
and in your browser go to:
http://localhost:8000/store