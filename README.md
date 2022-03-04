# cpf-app-xml-generator
Parse csv file that list all the offers of a French school to generate xml file that will feed government CPF new App. https://play.google.com/store/apps/details?id=fr.icdc.sl6.app Mon compte formation

# App preview
![preview of app on store](https://raw.githubusercontent.com/73k05/cpf-app-xml-generator/master/static/images/preview.png)

## Install deps
`pip3 install -r requirements.txt`

## Start server
```python3.9 restart.py```

### PROD With SSL
```python3.9 __main__.py --ssl -d ./upload --password * --env PROD > server.log```

### DEV Without SSL
```python3.9 __main__.py -d ./upload --password * --env DEV > server.log```

## XSD validation
https://www.freeformatter.com/xml-validator-xsd.html

## Server fault restart
Add

```
00 */8 * * * /bin/bash -l -c 'currentDate=`date +"\%Y-\%m-\%d"`;cd /root/cpf-app-xml-generator; cp logs/server.log logs/`echo $currentDate`.log;python3.7 server_restart.py > logs/server.log 2>&1 &'
```

to ```crontab -e```

## Open and save input file
Use ```trame.csv``` to base your example and open/save with ```utf-8``` encoding. Ouput xml file will be ```iso-8859-1``` encoded. Please use *libreoffice* to edit trame.csv and not office

### Open
![open trame.csv](https://raw.githubusercontent.com/73k05/cpf-app-xml-generator/master/resources/images/open_csv.png)

### Save
![save tram.csv](https://raw.githubusercontent.com/73k05/cpf-app-xml-generator/master/resources/images/save_csv.png)

![Version 1.4](http://img.shields.io/badge/version-v1.4-green.svg)
![Python 3.8](http://img.shields.io/badge/python-3.8-blue.svg)
[![MIT License](http://img.shields.io/badge/license-MIT%20License-blue.svg)](https://github.com/sc0tfree/updog/blob/master/LICENSE)
[![sc0tfree Twitter](http://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Follow)](https://twitter.com/sc0tfree)

<p>
  <img src="https://sc0tfree.squarespace.com/s/updog.png" width=85px alt="updog"/>
</p>

Updog is a replacement for Python's `SimpleHTTPServer`. 
It allows uploading and downloading via HTTP/S, 
can set ad hoc SSL certificates and use HTTP basic auth.

<p align="center">
  <img src="https://sc0tfree.squarespace.com/s/updog-screenshot.png" alt="Updog screenshot"/>
</p>

## Installation

Install using pip:

`pip3 install updog`

## Usage

`updog [-d DIRECTORY] [-p PORT] [--password PASSWORD] [--ssl]`

| Argument                            | Description                                      |
|-------------------------------------|--------------------------------------------------| 
| -d DIRECTORY, --directory DIRECTORY | Root directory [Default=.]                       | 
| -p PORT, --port PORT                | Port to serve [Default=9090]                     |
| --password PASSWORD                 | Use a password to access the page. (No username) |
| --ssl                               | Enable transport encryption via SSL              |
| --version                           | Show version                                     |
| -h, --help                          | Show help                                        |

## Examples

**Serve from your current directory:**

`updog`

**Serve from another directory:**

`updog -d /another/directory`

**Serve from port 1234:**

`updog -p 1234`

**Password protect the page:**

`updog --password examplePassword123!`

*Please note*: updog uses HTTP basic authentication.
To login, you should leave the username blank and just
enter the password in the password field.

**Use an SSL connection:**

`updog --ssl`

## Thanks

A special thank you to [Nicholas Smith](http://nixmith.com) for
designing the updog logo.
