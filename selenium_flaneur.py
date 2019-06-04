#!/usr/bin/env python
# coding: utf-8
import datetime
import re
import urllib
import urllib.request

from io import BytesIO
from urllib.parse import urlparse

import piexif
import pytz

from PIL import Image, ExifTags
from babel.dates import format_datetime, get_timezone
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def get_event_description(event_id):
    driver.get(f'https://www.facebook.com/events/{event_id}/')
    data = driver.find_element_by_xpath("//div[@data-testid='event-permalink-details']")
    return {'description': data.text}


def launch_browser():
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')  # required when running as root user. otherwise you would get no sandbox errors.
    driver = webdriver.Chrome(options=options)
    return driver


def get_latest_post():
    post_id = 'photos/a.195591940806855/850644405301602'
    with open('posts.txt') as posts:
        for line in posts:
            post_id = line.replace('\n', '')
    return post_id


def get_post(post_id):
    driver.get('https://www.facebook.com/FlaneurSaarbruecken/{}/?type=3&theater'.format(post_id))
    xpath_content = "//div[@class='_5pbx userContent _3576']"
    content = driver.find_element_by_xpath(xpath_content)
    bs_html = soup(content.get_attribute('innerHTML'), "html5lib")
    return bs_html


def build_links(bs_html):
    from_questionmark = re.compile('\?.*')
    fbclid = re.compile('[\&|\?]fbclid=.*')
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
            event = get_event_description(event_id)
            if event.get('description', None):
                event_details = '<label for="item-{}">&nbsp;</label><input type="checkbox" name="one" id="item-{}"><span class="hide">Beschreibung der Veranstalter*innen: <i>{}</i></span>'.format(event_id, event_id, event.get('description').replace('\n', '{breakline}'))
        # build link
        link.replace_with('[{}]({}){} '.format(link.text, link['href'], event_details))


def download_image(driver, file_date):
    img = driver.find_element_by_xpath('//a[@rel="theater"]//img')

    # Download Image
    img_src = img.get_attribute('src')
    img_path = content_path + 'images/' + file_date + '.jpg'
    urllib.request.urlretrieve(img_src, img_path)
    return img_path


def resize_image(img_path):
    # Resize Image
    img = Image.open(img_path)
    x, y = img.size
    resized = img.resize((int(x/(x/722)), int(y/(x/722))))
    resized.save(img_path)


def update_exif(img_path, file_date):
    # Add Exif Data
    exif = piexif.load(img_path)
    o = BytesIO()
    thumb_im = Image.open(img_path)
    thumb_im.thumbnail((50, 50), Image.ANTIALIAS)
    thumb_im.save(o, "jpeg")
    thumbnail = o.getvalue()

    exif['thumbnail'] = thumbnail
    zeroth_ifd = {piexif.ImageIFD.Artist: 'Sascha Markus', piexif.ImageIFD.Copyright: '(c) 2019 Sascha Markus'}
    exif["0th"] = zeroth_ifd
    piexif.insert(piexif.dump(exif), content_path + 'images/' + file_date + '.jpg')


def build_content(bs_html, file_date):
    # Build Post
    lines = list()
    leading_blanks = re.compile('^ *')
    for para in bs_html.find('body').contents:
        for con in para.contents:
            if con.name == 'br':
                lines.append('\n\n')
            else:
                lines.append(leading_blanks.sub('', str(con).replace('{breakline}', '<br/>')))
                if not lines[-1].startswith('***'):
                    lines[-1] = lines[-1].replace('*', '\\*')
        lines.append('\n\n')
    rst_image = "![{}]({{static}}images/{}.jpg)".format(lines[0], file_date)
    lines = [rst_image, '\n', '\n'] + lines
    return lines


def get_dates(driver):
    date = driver.find_element_by_class_name('timestampContent')
    date_utime = date.find_element_by_xpath('..').get_attribute('data-utime')

    server_tz = get_timezone('US/Pacific')
    timestamp = datetime.datetime.fromtimestamp(int(date_utime), server_tz)

    fb_date = format_datetime(server_dt, 'EEEE, dd.MM.yyyy H:mm', tzinfo=server_tz, locale='de_DE')
    rst_date = format_datetime(server_dt, 'yyyy-M-dd H:mm', tzinfo=server_tz, locale='de_DE')
    file_date = format_datetime(server_dt, 'yyyy-M-dd-H-mm', tzinfo=server_tz, locale='de_DE')
    return rst_date, file_date, fb_date


def build_prefix(fb_date, rst_date):
    prefix = """Title: Beitrag vom {}
Date: {}
Category: Ausgehen


""".format(fb_date, rst_date)
    return(prefix)


content_path = 'content/'
driver = launch_browser()

post_id = get_latest_post()
bs_html = get_post(post_id)

rst_date, file_date, fb_date = get_dates(driver)

prefix = build_prefix(fb_date, rst_date)

img_path = download_image(driver, file_date)
resize_image(img_path)
update_exif(img_path, file_date)

build_links(bs_html)
content = build_content(bs_html, file_date)

out_fname = content_path + 'post_' + file_date + '.md'
with open(out_fname, 'w') as ofile:
    print('writing', out_fname)
    ofile.write(prefix)
    ofile.write(''.join(content))
