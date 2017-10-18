# leboncoin_spider
A python script scrapping the Leboncoin's URL you give it every 30 seconds and send you an e-mail when new offers pop.

##### Dependencies:
- Python 3.5
- libsmtp
- scrapy

Resolve with:
```bash
pip3 install libsmtp scrapy
```
___

##### Usage:
```bash
python3.5 run.py [-u url] [-t email_to] [-f email_from] [-p email_password]
```
- All the parameters can be either provided through the `lbcscrap.config.json` file or through command line parameter (see previous example).
- If the parameters are provided both via the command line and the `lbcscrap.config.json` file, command line arguments will have priority.
- The URL must be a valid [Leboncoin.com](https://www.leboncoin.fr) URL. Make your research on the site, provide all your filters using Leboncoin's filter engine, click 'Rechercher' and then copy the URL directly from your browser.
- Mail adresses provided must be valid GMAIL e-mail adresses.
- If no "email_from" (-f parameter) address is provided, "email_to" (-t parameter) address will be taken as "email_from" address by default.
