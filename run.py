import os.path
import sys
import json
import time
import logging

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

FILENAME = "res.json"
previous_count = 0
previous_data = None
logger = logging.getLogger()


############################# UTILS ############################

def stringify(offer):
    res = offer['title'] + "\n"
    res += "Prix: --------- " + offer['price'] + "€ ---------\n"
    res += "Localisation: " + offer['location'] + "\n"
    res += "Date de publication: " + offer['date_pub'] + "\n"
    res += "URL: " + offer['href'] + "\n"
    return res

def send_mail(actual_count, data):
    print("[" + time.ctime() + "] :: SENDING AN EMAIL")

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = 'New offers found on Leboncoin!'

    message = 'New offers were found on Leboncoin! \n\n'
    count = 1
    for o in data:
        message += str(count) + " - "
        message += stringify(o)
        message += "\n\n"
        count += 1

    message += "Hope you find your stuff :)!"

    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(email_from, email_password)
    mailserver.sendmail(email_from, email_to, msg.as_string())
    mailserver.quit()


def delete_res():
    if os.path.exists(FILENAME):
        os.remove(FILENAME)


def run_scrapper():
    print("[" + time.ctime() + "] :: Running scrapper for: " + start_url)
    os.system("scrapy runspider crawler.py --nolog -a start_url=" + start_url + " -o " + FILENAME)


# check if an offer has been added and returns the list of new offers
def offer_added(previous_data, new_data):
    if previous_data is None or new_data is None:
        return []
    return [o for o in new_data if o not in previous_data]


def get_arg(argv, option):
    if option in argv:
        index = argv.index(option)
        if not index == len(argv) - 1 and not argv[index + 1].startswith('-'):
            return argv[index + 1]
    return None

################################################################

if len(sys.argv) < 3 and not os.path.exists('lbcscrap.config.json'):
    print('You need to fill at least the lbcscrap.config.jsonor to provide arguments.')
    print('Usage: run.py [-u url] [-t email_to] [-f email_from] [-p email_password]')
    exit(1)

start_url = get_arg(sys.argv, "-u")
email_from = get_arg(sys.argv, "-f")
email_to = get_arg(sys.argv, "-t")
email_password = get_arg(sys.argv, "-p")

if None in [start_url, email_to, email_password]:
    try:
        conf = None
        if os.path.exists('lbcscrap.config.json'):
            with open('lbcscrap.config.json') as config:
                conf = json.load(config)
                if start_url == None:
                    start_url = conf['url']
                if email_from == None:
                    email_from = conf['email_from']
                if email_to == None:
                    email_to = conf['email_to']
                if email_password == None:
                    email_password = conf['email_password']

        if None in [start_url, email_to, email_password] or "" in [start_url, email_to, email_password]:
            raise ValueError("Some arguments can't be found in the script call nor in the config file.")

    except ValueError:
        print("Some arguments can't be found in the arguments provided nor in the config file.")
        print("Be sure to provide at least one these (arguments prioritary).")
        exit(1)

if email_from == None or email_from == "":
    email_from = email_to

# deleting the file if it already exists
delete_res()

print('\n')
# running the scraper a first time
run_scrapper()

while True:
    # opening the results file
    with open(FILENAME, 'r') as file:
        data = json.load(file)
        file.close()

        # getting the count and the first page's items
        actual_count = int(data[0]['count'])

        # sending a mail if the count has changed and an offer has been added
        if not previous_count == 0 and not actual_count == 0:
            news = offer_added(previous_data, data[1:])
            if previous_data != None and len(news) != 0:
                send_mail(actual_count, news)

        previous_data = data[1:]
        previous_count = actual_count

    delete_res()

    time.sleep(30)
    run_scrapper()
