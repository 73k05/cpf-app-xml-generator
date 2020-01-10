# cpf-app-xml-generator
Parse csv file that list all the offers of a French school to generate xml file that will feed government CPF new App. https://play.google.com/store/apps/details?id=fr.icdc.sl6.app Mon compte formation

# App preview


## Start server
```python simple_http_server.py```

## XSD validation
https://www.freeformatter.com/xml-validator-xsd.html

## Server fault restart
Add ```00 */8 * * * /bin/bash -l -c 'cd /root/cpf-app-xml-generator/;python3.7 server_restart.py > server.log 2>&1 &'``` to ```crontab -e```
