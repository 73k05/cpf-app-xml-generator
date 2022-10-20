# CPF EDOF générateur de fichier XML
Les citoyens français ont la possibilité d'utiliser leur Compte Professionel de Formation (CPF) pour se former auprés d'organismes certifiants. Afin de retrouver la liste des formations de votre organisme (OF) sur la plateforme (et par conséquent l'application) proposée par l'Espace des Organismes de Formation (EDOF) du gouvernement il est nécessaire de générer un fichier XML.

**Si vous êtes organisme de formation, cette page est faite pour vous!**

Ce projet contient le code serveur BO développé en Python avec un petit front designé avec Bootstrap. Les sources permettent de déployer un petit Site Web grâce à la librairie Flask. Cette plateforme est hébergée sur votre ordinateur en local ou en ligne sur un serveur VPS par exemple. Une fois le serveur déployé très simplement, il suffit de téléverser un fichier CSV contenant toutes les formations EDOF lignes par ligne de votre Organisme de Formation. Chaque formation correspond à une ligne du fichier CSV et chaque colonne est une balise du fichier XML qui sera généré en sortie.

Parse csv file that list all the offers of a French school to generate xml file that will feed government CPF new App. https://play.google.com/store/apps/details?id=fr.icdc.sl6.app Mon compte formation

# App preview
![preview of app on store](https://raw.githubusercontent.com/73k05/cpf-app-xml-generator/master/static/images/preview.png)

# Installation

## Install dependencies
`pip3 install -r requirements.txt`

## Start server

### DEV Without SSL
This command should be enough to start the serveur and test locally:

```python3 __main__.py -d "./upload" --password "*" --env DEV > server.log```

### PROD With SSL (PROD: Advanced Users)
```python3 restart.py```

**Or**

```python3 __main__.py --ssl -d "./upload" --password "*" --env PROD > server.log```

# XSD validation
Always validate your generated XML file before submitting it to EDOF:
https://www.freeformatter.com/xml-validator-xsd.html

# Server fault restart
Sometimes the server crashes for some reason, we periodically restart it with crontab. Add this line to ```crontab -e```

```
00 */8 * * * /bin/bash -l -c 'currentDate=`date +"\%Y-\%m-\%d"`;cd /root/cpf-app-xml-generator; cp logs/server.log logs/`echo $currentDate`.log;python3 restart.py > logs/server.log 2>&1 &'
```

# Certificates (PROD: Advanced Users)
Use LetsEncrypt to create certificates on your machine: https://certbot.eff.org/instructions?ws=other&os=ubuntufocal Then modify `config/config.ini` file to update paths:
```
CERTIFICATE_PATH = /etc/letsencrypt/live/*/fullchain.pem
PRIVATE_KEY_PATH = /etc/letsencrypt/live/*/privkey.pem         
```

# Open and save input file
Use ```trame.csv``` to base your example and open/save with ```utf-8``` encoding. Ouput xml file will be ```iso-8859-1``` encoded. Please use *libreoffice* to edit trame.csv and not office

## Open
![open trame.csv](https://raw.githubusercontent.com/73k05/cpf-app-xml-generator/007d078a9197316decba03f4fc01c3a85d976d74/resources/images/open_csv.png)

## Save

![save tram.csv](https://github.com/73k05/cpf-app-xml-generator/blob/007d078a9197316decba03f4fc01c3a85d976d74/resources/images/save_csv.png)


# UpDog dependency is used to serve & upload files (Advanced Users)

![Version 1.4](http://img.shields.io/badge/version-v1.4-green.svg)
![Python 3.10.6](http://img.shields.io/badge/python-3.8-blue.svg)
[![MIT License](http://img.shields.io/badge/license-MIT%20License-blue.svg)](https://github.com/sc0tfree/updog/blob/master/LICENSE)

<p>
  <img src="https://sc0tfree.squarespace.com/s/updog.png" width=85px alt="updog"/>
</p>

Updog is a replacement for Python's `SimpleHTTPServer`. 
It allows uploading and downloading via HTTP/S, 
can set ad hoc SSL certificates and use HTTP basic auth.

<p align="center">
  <img src="https://sc0tfree.squarespace.com/s/updog-screenshot.png" alt="Updog screenshot"/>
</p>

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
