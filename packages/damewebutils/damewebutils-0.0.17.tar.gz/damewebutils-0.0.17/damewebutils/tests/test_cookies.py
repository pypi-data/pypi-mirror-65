#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2019  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with damewebutils; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,


from unittest import TestCase
from http import cookies
import requests

class TestCookies(TestCase):

    def test_cookies(self):
        C = cookies.SimpleCookie()
        C["fig"] = "newton"
        C["sugar"] = "water"
        self.assertEqual(str(C["fig"]), "Set-Cookie: fig=newton")
        self.assertEqual(str(C["sugar"]), "Set-Cookie: sugar=water")
        C["rocky"] = "road"
        C["rocky"]["path"] = "/cookie"
        self.assertEqual(str(C.output(header="Cookie:")), "Cookie: fig=newton\r\nCookie: rocky=road; Path=/cookie\r\nCookie: sugar=water")
        self.assertEqual(str(C.output(attrs=[], header="Cookie:")), 'Cookie: fig=newton\r\nCookie: rocky=road\r\nCookie: sugar=water')

    def test_cookies2(self):
        C = cookies.SimpleCookie()
        C.load("chips=ahoy; vienna=finger") # load from a string (HTTP header)
        self.assertEqual(str(C), "Set-Cookie: chips=ahoy\r\nSet-Cookie: vienna=finger")

    def test_cookies3(self):
        C = cookies.SimpleCookie()
        C["oreo"] = "doublestuff"
        C["oreo"]["path"] = "/"
        self.assertEqual(str(C), "Set-Cookie: oreo=doublestuff; Path=/")

    def test_cookies4(self):
        C = cookies.SimpleCookie()
        C["twix"] = "none for you"
        self.assertEqual(C["twix"].value, "none for you")

    def test_cookies5(self):
        C = cookies.SimpleCookie()
        C["number"] = 7 # equivalent to C["number"] = str(7)
        C["string"] = "seven"
        self.assertEqual(C["number"].value, '7')
        self.assertEqual(C["string"].value, "seven")

    def test_session(self):
        s = requests.Session()
        s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
        r = s.get("http://httpbin.org/cookies")
        self.assertEqual(r.text, '{\n  "cookies": {\n    "sessioncookie": "123456789"\n  }\n}\n')
