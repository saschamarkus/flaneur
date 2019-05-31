#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from os import path

AUTHOR = 'Sascha Markus'
SITENAME = 'Der Flaneur'
SITEURL = ''

PATH = 'content'
OUTPUT_PATH = 'public'


TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'de'

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
#FEED_ATOM = 'feeds/all.atom.xml'
#FEED_RSS = 'feeds/all.rss.xml'
FEED_ALL_ATOM = 'feeds/atom.xml'
FEED_ALL_RSS = 'feeds/rss.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

THEME = "m.css/pelican-theme"
THEME_STATIC_DIR = 'static'
DIRECT_TEMPLATES = ['index']
#M_CSS_FILES = ['https://fonts.googleapis.com/css?family=Libre+Baskerville:400,400i,700,700i%7CSource+Code+Pro:400,400i,600',
#                               '/static/m-light.css']
M_CSS_FILES = ['/static/m-light.compiled.css']
M_THEME_COLOR = '#4267b2'
M_FAVICON = ('favicon.ico', 'image/x-ico')
M_SITE_LOGO = path.join(SITEURL, "/images/flaneur.png")

PLUGIN_PATHS = ['m.css/pelican-plugins']
PLUGINS = ['m.htmlsanity', 'm.images', 'm.components', 'm.link']
M_IMAGES_REQUIRE_ALT_TEXT = False
M_HIDE_ARTICLE_SUMMARY = True
M_LINKS_FOOTER1 = [('Der Flaneur', '/'),
                ('Über den Flaneur', path.join(SITEURL, 'pages/der-flaneur.html')),
                ('Der Flaneur bei Patreon', 'https://patreon.com/derflaneur'),
                ('Impressum', path.join(SITEURL, 'pages/impressum.html')),
                ('Datenschutz', path.join(SITEURL, 'pages/datenschutz.html')),
                ('Atom-Feed', path.join(SITEURL, 'feeds/all.atom.xml')),
                ('RSS-Feed', path.join(SITEURL, 'feeds/all.rss.xml'))]

STATIC_PATHS = [
                'images',
                'extra',
                ]

EXTRA_PATH_METADATA = {
                path.join(SITEURL, 'extra/favicon.ico'): {'path': 'favicon.ico'},
                }

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('Facebook', 'https://www.facebook.com/FlaneurSaarbruecken/'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 3

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
