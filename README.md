# cpf-app-xml-generator
Parse csv file that list all the offers of a French school to generate xml file that will feed government CPF new App

## Start server
```python simple_http_server.py```

## XSD validation
https://www.freeformatter.com/xml-validator-xsd.html

## Server fault restart
Add ```0 23 * * * /bin/bash -l -c 'cd cpf-app-xml-generator/;nohup python simple_http_server.py > server.log 2>&1 &'``` to ```crontab -e```
