# -*- coding: utf-8 -*-
"""
/***************************************************************************
 HelloWorld
                                 A QGIS plugin
 Hello World Plugin
                             -------------------
        begin                : 2013-06-18
        copyright            : (C) 2013 by Joana Simoes/FAO
        email                : info@doublebyte.net
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
appVers=1.21

def name():
    return "Diagram Legend Plugin"
def description():
    return "Diagram Legend Plugin"
def version():
    #return "Version 1.1"
    return "Version" + appVers
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "1.6"
def qgisMinimumVersion():
    return "2.99"
def classFactory(iface):
    from diagleg import DiagLeg
    return DiagLeg(iface)
def authorName():
  return "Joana Simoes"