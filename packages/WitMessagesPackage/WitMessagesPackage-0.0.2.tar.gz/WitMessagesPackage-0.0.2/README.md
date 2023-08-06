# WitAdvisor Notifications

[![N|Solid](https://ver2.witadvisor.com.ar/assets/media/logos/logo-light.png)](https://ver2.witadvisor.com.ar/)

This package will generate a service to encapsulate the notifications by 3 different systems.

  - Email: 
    * [Sengrid]
  - SMS: 
    * [Infobip]
    * [Kyrabo]
  - WhatsApp:
    * [Botmaker]

### Generating distribution archives [PIP-PACKAGE]
> Make sure you have the latest versions of setuptools and wheel installed:
```sh
$ cpython3 -m pip install --user --upgrade setuptools wheel
```
> Now run this command from the same directory where setup.py is located:
```sh
$ python3 setup.py sdist bdist_wheel
```
> This command should output a lot of text and once completed should generate two files in the dist directory.

### Uploading the distribution archives
```sh
$ python3 -m pip install --user --upgrade twine
$ python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```
> You will be prompted for a username and password. For the username, use __token__. For the password, use the token value, including the pypi- prefix (nano ./pypirc).

### Installing your newly uploaded package
```sh
$ pip install WitMessagesPackage
```

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
[Sengrid]: <https://github.com/sendgrid/sendgrid-python/>
[Infobip]: <https://dev.infobip.com/#programmable-communications/sms/send-sms-message>
[Kyrabo]: <http://149.56.207.9/app/api>
[Botmaker]: <https://botmakeradmin.github.io/docs/es/#/messages-api>
[PIP-PACKAGE]: <https://packaging.python.org/tutorials/packaging-projects/>
