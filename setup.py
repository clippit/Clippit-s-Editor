# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe

setup(windows=[{'script':'main.pyw','icon_resources':[(1,"main.ico")]}],options={'py2exe':{'includes':['sip','PyQt4']}})