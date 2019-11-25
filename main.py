from __future__ import unicode_literals
import re
import os
import requests
import youtube_dl
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('-u', "--url", nargs='+', help='url à envoyer')
args = parser.parse_args()

for url in args.url:
    dossier = input("Nom du dossier : ")
    os.mkdir('/root/Téléchargements/'+dossier+'/')
    os.chdir('/root/Téléchargements/'+dossier+'/')
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links_with_text = [a['href'] for a in soup.find_all('a', href=True) if a.text]

    count = 0
    for i in links_with_text:
        if re.search(r'course', i) != None:
            page_to_download = "https://www.college-de-france.fr/"+ i
            print(page_to_download)
            count += 1
            zero_before = str("{:02d}".format(count))

            ydl_opts = {
                'verbose': True,
                'outtmpl': '{0}-%(title)s.%(ext)s'.format(zero_before),
                'ratelimit': 1000000
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([page_to_download])
