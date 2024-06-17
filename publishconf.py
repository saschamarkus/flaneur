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
#SITEURL = 'https://der-flaneur.rocks'
SITEURL = 'https://saschamarkus.gitlab.io/flaneur/'
RELATIVE_URLS = True

FEED_DOMAIN = SITEURL


# M_LINKS_FOOTER1 = [('Der Flaneur', '/'),
#                 ('Über den Flaneur', path.join(SITEURL, 'pages/der-flaneur.html')),
#                 ('Impressum', path.join(SITEURL, 'pages/impressum.html')),
#                 ('Datenschutz', path.join(SITEURL, 'pages/datenschutz.html'))]


DELETE_OUTPUT_DIRECTORY = False

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
