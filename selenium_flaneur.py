#!/usr/bin/env python
# coding: utf-8
import datetime  
import json
import re
import requests
import urllib
import urllib.request

from os import environ
from urllib.parse import urlparse

from bs4 import BeautifulSoup as soup 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def login(user, password):
    elem = driver.find_element_by_id("email")
    elem.send_keys(user)
    elem = driver.find_element_by_id("pass")
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)


options = Options()
options.add_argument("--disable-notifications")
options.add_argument('--headless')
options.add_argument('--no-sandbox')  # required when running as root user. otherwise you would get no sandbox errors.
driver = webdriver.Chrome(options=options)

driver.get("http://www.facebook.com")

login(environ['facebook_user'], environ['facebook_pwd'])

driver.get("https://developers.facebook.com/tools/explorer/")
button_div = driver.find_elements_by_xpath('//button/div/div[text()="Get Access Token"]')
button_div[0].click()
auth_key = driver.find_element_by_xpath('//input[@placeholder="Zugriffsschlüssel"]').get_attribute('value')


post_id = '848667262165983'
with open('posts.txt') as posts:
    for line in posts:
        post_id = line.replace('\n', '')

driver.get('https://www.facebook.com/FlaneurSaarbruecken/{}/?type=3&theater'.format(post_id))

close_image = driver.find_element_by_xpath("//u[contains(text(), 'Schließen')]")
if close_image:
    close_image.find_element_by_xpath("ancestor::a").click()

xpath_content = "//div[@class='_5pbx userContent _3576']"
content = driver.find_element_by_xpath(xpath_content)

bs_html = soup(content.get_attribute('innerHTML'), "html5lib")

def get_event_data(auth_key, event_id):
    event = dict()
    graph_data = requests.get("https://graph.facebook.com/v3.2/{}?access_token={}".format(event_id, auth_key))
    if graph_data.ok:
        event = graph_data.json()
        event['@context'] = 'http://schema.org/'
        event['@type'] = 'Event'
        event['enddate'] = event.pop('end_time', None)
        event['startdate'] = event.pop('start_time', None)
        event['url'] = 'https://www.facebook.com/' + event.pop('id', event_id)
        event.pop('event_times', None)

        location = event.pop('place', dict())
        location['@type'] = 'Place'
        location['url'] = 'https://www.facebook.com/' + location.pop('id', '')
        
        address = location.pop('location', dict())
        address['@type'] = 'PostalAddress'
        address['addressLocality'] = address.pop('city', '') + ', ' + address.pop('country', '')
        address['streetAddress'] = address.pop('street', '')
        address['postalCode'] = address.pop('zip', '')
        address.pop('located_in', '')
        location['address'] = address
        
        geo = {'@type': 'GeoCoordinates'}
        geo['latitude'] = address.pop('latitude', None)
        geo['longitude'] = address.pop('longitude', None)
        location['geo'] = geo

        event['location'] = location
    else:
        print(graph_data.status_code, event_id)
    return event

# is the auth_key working? check a known event
get_event_data(auth_key, '1975295982491804')['name']

#desc = get_event_data(auth_key, '2117680151587265')['description']

#desc.replace('\n', '{breakline}')

from_questionmark= re.compile('\?.*')
fbclid = re.compile('[\&|\?]fbclid=.*')
all_events = list()
for link in bs_html.find_all('a'):
    # make relative paths absolute
    if link['href'].startswith('/'):
        link['href'] = 'https://www.facebook.com' + link['href']
    # remove extra parameters
    if link['href'].startswith('https://www.facebook.com/'):
        link['href'] = from_questionmark.sub('', link['href'])
    # prepare external links
    if link['href'].startswith('https://l.facebook.com/l.php'):
        link['href'] = urllib.parse.parse_qs(urlparse(link['href']).query)['u'][0]
    # remove facebook tracking
    link['href'] = fbclid.sub('', link['href'])
    event = dict()
    event_details = ''
    if 'facebook.com/events/' in link['href']:
        event_id = link['href'].split('/')[-2]
        event = get_event_data(auth_key, event_id)
        if event.get('description', None):
            event_details = '<label for="item-{}">&nbsp;</label><input type="checkbox" name="one" id="item-{}"><span class="hide">Beschreibung der Veranstalter*innen: <i>{}</i></span>'.format(event_id, event_id, event.get('description').replace('\n', '{breakline}'))
        if event:
            json_ld = '<script type="application/ld+json">{}</script>'.format(json.dumps(event))
            all_events.append(json_ld)
    # build rst link
    link.replace_with('[{}]({}){} '.format(link.text, link['href'], event_details))

content_path = 'content/'

# prepare post header

date = driver.find_element_by_class_name('timestampContent')
fb_date = date.find_element_by_xpath('..').get_attribute('title')
rst_date = datetime.datetime.strptime(fb_date, '%d.%m.%y, %H:%M').strftime('%Y-%m-%d %H:%M')
filename_date = datetime.datetime.strptime(fb_date, '%d.%m.%y, %H:%M').strftime('%Y-%m-%d-%H-%M')

img = driver.find_element_by_xpath('//a[@rel="theater"]//img')

# Download Image

img_src = img.get_attribute('src')

img_path = content_path + 'images/' + filename_date + '.jpg'

urllib.request.urlretrieve(img_src, img_path)

# Resize Image

from PIL import Image, ExifTags

img = Image.open(img_path)

x, y = img.size

resized = img.resize((int(x/(x/722)), int(y/(x/722)))) 

resized.save(img_path)

# Add Exif Data

import piexif

exif = piexif.load(img_path)

import io

o = io.BytesIO()
thumb_im = Image.open(img_path)
thumb_im.thumbnail((50, 50), Image.ANTIALIAS)
thumb_im.save(o, "jpeg")
thumbnail = o.getvalue()

exif['thumbnail'] = thumbnail

zeroth_ifd = {piexif.ImageIFD.Artist: 'Sascha Markus', piexif.ImageIFD.Copyright: '(c) 2019 Sascha Markus'}

exif["0th"] = zeroth_ifd

piexif.insert(piexif.dump(exif), content_path + 'images/' + filename_date + '.jpg')

# Build Post

lines = list()

leading_blanks= re.compile('^ *')
for para in bs_html.find('body').contents:
    # print(para.name)
    for con in para.contents:
        #print('>>>', con, '<<<', con.name)
        if con.name == 'br':
            lines.append('\n\n')
        else:
            lines.append(leading_blanks.sub('', str(con).replace('{breakline}', '<br/>')))
    lines.append('\n\n')
for ld in all_events:
    if ld:
        lines.append('  ' + ld + '\n')

rst_image = "![{}]({{static}}images/{}.jpg)".format(lines[0], filename_date)

prefix = """Title: Beitrag vom {}
Date: {}
Category: Ausgehen

""".format(fb_date, rst_date)

lines = [rst_image, '\n', '\n'] + lines

with open(content_path + 'post_' + filename_date+ '.md', 'w') as ofile:
    ofile.write(prefix)
    ofile.write(''.join(lines))
