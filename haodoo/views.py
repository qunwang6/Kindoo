# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re, requests, logging
from Kindoo.apps_config import APPS_CONFIG as APPS_CONFIG
from django.shortcuts import render
from django.http import HttpResponse
from django import forms

HOST = "http://www.haodoo.net"
logger = logging.getLogger("django") #init python logger instance

class formBook(forms.Form):
    email = forms.EmailField()
    targetId = forms.CharField()

def formHandler(req):
    if req.method == 'POST':
        form = formBook(req.POST)
        if form.is_valid():
            requestHandler(req.POST)
    else:
        form = formBook()
    return render(req, 'form.html', {'form': form})

def requestHandler(parms):
    url = HOST + '/?M=book&P='+parms.get('targetId')
    req = requests.get(url)

    if(req.status_code == 200):
        matchs = re.findall(r'DownloadPrc\(\'(.{1,6})\'\)', req.text)
        if(matchs[0]):
            filename = matchs[0] + '.prc'
            file = requests.get(HOST + "/?M=d&P="+filename, stream=True)
            if(file.status_code == 200):
                if(storeResource(file, 'files/' +filename)):
                    sendResourceByEmail(parms.get('email'), 'files/' +filename)
                    return True
        else:
            logger.error("unexpected error")
    return False


def storeResource(file, filename):
    try:
        with open(filename, 'wb+') as destination:
            for chunk in file.iter_content(chunk_size=1024):
                if(chunk):
                    destination.write(chunk)
        return True
    except IOError:
        logger.error("Download: File not exist")
        return False

def sendResourceByEmail(email, filename):
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
