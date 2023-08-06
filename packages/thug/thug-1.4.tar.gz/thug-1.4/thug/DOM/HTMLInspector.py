#!/usr/bin/env python
#
# HTMLInspector.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA

import os
import logging

import six.moves.configparser as ConfigParser

import bs4

log = logging.getLogger("Thug")


class HTMLInspector(object):
    def __init__(self):
        self.init_config()
        self.init_select()

    def init_config(self):
        conf_file = os.path.join(log.configuration_path, 'inspector.conf')
        self.config = ConfigParser.ConfigParser()
        self.config.read(conf_file)

    def init_select(self):
        self.html_select = self.config.get('html', 'select').split(',')

    def run(self, html, parser = "html.parser"):
        soup = bs4.BeautifulSoup(html, parser)
        return self.clean(soup) if html else soup

    def clean(self, soup):
        modified = False

        for s in self.html_select:
            for p in soup.select(s):
                p.extract()
                modified = True

        if modified:
            log.ThugLogging.add_behavior_warn(description = "[HTMLInspector] Detected potential code obfuscation",
                                              snippet     = soup.get_text(),
                                              method      = "HTMLInspector deobfuscation")

        return soup
