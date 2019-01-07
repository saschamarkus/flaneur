#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
#SITEURL = 'https://www.der-flaneur.rocks'
#SITEURL = ''
SITEURL = 'https://saschamarkus.gitlab.io/flaneur'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

M_SITE_LOGO = path.join(SITEURL, "/images/flaneur.png")
M_LINKS_FOOTER1 = [('Der Flaneur', '/'),
                ('Über den Flaneur', path.join(SITEURL, 'pages/der-flaneur.html')),
                ('Impressum', path.join(SITEURL, 'pages/impressum.html')),
                ('Datenschutz', path.join(SITEURL, 'pages/datenschutz.html'))]

M_CSS_FILES = ['https://fonts.googleapis.com/css?family=Libre+Baskerville:400,400i,700,700i%7CSource+Code+Pro:400,400i,600',
                               path.join(SITEURL, '/static/m-light.css')]

STATIC_PATHS = [
                path.join(SITEURL, 'images'),
                path.join(SITEURL, 'extra'),
                ]

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
