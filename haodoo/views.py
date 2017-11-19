# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re, requests, logging
from Kindoo.apps_config import APPS_CONFIG as APPS_CONFIG
from django.shortcuts import render
from django.http import HttpResponse

HOST = "http://www.haodoo.net"
EMAIL = "ko19950314@kindle.com"
logger = logging.getLogger("django") #init python logger instance

def viewBook(req):
    parms = req.GET
    if(getBook(bid=parms.get('id'))):
        html = "Done!"
    else:
        html = "Fuck!"
    return HttpResponse(html)

def getBook(bid):
    url = HOST + '/?M=book&P='+bid
    req = requests.get(url)

    if(req.status_code == 200):
        matchs = re.findall(r'DownloadPrc\(\'(.{1,6})\'\)', req.text)
        if(matchs[0]):
            filename = matchs[0] + '.prc'
            file = requests.get(HOST + "/?M=d&P="+filename, stream=True)
            if(file.status_code == 200):
                if(downloadBookHandler(file, filename)):
                    sendBookHandler(EMAIL, filename)
                    return True
        else:
            logger.error("unexpected error")
    return False


def downloadBookHandler(file, filename):
    filename = 'files/' + filename
    try:
        with open(filename, 'wb+') as destination:
            for chunk in file.iter_content(chunk_size=1024):
                if(chunk):
                    destination.write(chunk)
        return True
    except IOError:
        logger.error("Download: File not exist")
        return False

def sendBookHandler(email, filename):
    filename = 'files/' + filename
    try:
        file = open(filename, "r")
        req = requests.post(APPS_CONFIG['MAILGUN']['api_url'],
            auth=("api", APPS_CONFIG['MAILGUN']['api_key']),
            files=[("attachment", file)],
            data={"from": APPS_CONFIG['MAILGUN']['user'] + "@" + APPS_CONFIG['MAILGUN']['domain'],
                  "to": email,
                  "subject": "Kindoo: " + filename,
                  "text": "Send from Kindoo\n"
                  })

        if(req.status_code == 200):
            logger.error("Your book is good to go!")
        else:
            logger.error("error with the email service")

    except IOError:
        logger.error("Send: File not exist")
