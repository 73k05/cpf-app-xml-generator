# cpf-app-xml-generator
Parse csv file that list all the offers of a French school to generate xml file that will feed government CPF new App. https://play.google.com/store/apps/details?id=fr.icdc.sl6.app Mon compte formation

# App preview
![preview of app on store](https://raw.githubusercontent.com/73k05/cpf-app-xml-generator/master/resources/images/app_store.png)

## Start server
```python simple_http_server.py```

## XSD validation
https://www.freeformatter.com/xml-validator-xsd.html

## Server fault restart
Add

```
31 19 * * * /bin/bash -l -c 'currentDate=`date +"\%Y-\%m-\%d"`;cd /root/cpf-app-xml-generator; cp logs/server.log logs/`echo $currentDate`.log;python3.7 server_restart.py > logs/server.log 2>&1 &'
```

to ```crontab -e```

## Open and save input file
Use ```trame.csv``` to base your example and open/save with ```utf-8``` encoding. Ouput xml file will be ```iso-8859-1``` encoded. Please use *libreoffice* to edit trame.csv and not office

### Open
![open trame.csv](https://raw.githubusercontent.com/73k05/cpf-app-xml-generator/master/resources/images/open_csv.png)

### Save
![save tram.csv](https://raw.githubusercontent.com/73k05/cpf-app-xml-generator/master/resources/images/save_csv.png)
