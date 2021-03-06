# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DiagLeg
                                 A QGIS plugin
 Diagram Legend Plugin
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
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from diaglegdialog import DiagLegDialog


class DiagLeg:
    
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # Create the dialog and keep reference
        self.dlg = DiagLegDialog()
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/diagleg"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:2]
       
        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/diagleg_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
   

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/diagleg/icon.png"), \
            u"DiagLeg", self.iface.mainWindow())
            
	self.iface.registerMainWindowAction(self.action, "F7") # action1 is triggered by the F7 key
	QObject.connect(self.action, SIGNAL("triggered()"),self.keyActionF7)
                    
	# check if Raster menu available
	if hasattr(self.iface, "addPluginToRasterMenu"):
	  # Raster menu and toolbar available
	  #self.iface.addRasterToolBarIcon(self.action)
	  #self.iface.addPluginToRasterMenu("&My plugins", self.action)
	#else:
	  # there is no Raster menu, place plugin under Plugins menu as usual
	  self.iface.addToolBarIcon(self.action)
	  self.iface.addPluginToMenu("&GISforEAF", self.action)	  
                
    def unload(self):
	# check if Raster menu available and remove our buttons from appropriate
	# menu and toolbar
	if hasattr(self.iface, "addPluginToRasterMenu"):
	  #self.iface.removePluginRasterMenu("&My plugins",self.action)
	  #self.iface.removeRasterToolBarIcon(self.action)
	#else:
	  self.iface.removePluginMenu("&GISforEAF",self.action)
	  self.iface.removeToolBarIcon(self.action)
	  
	  self.iface.unregisterMainWindowAction(self.action)
	  
    def keyActionF7(self):
      self.run()
	  	  
    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            pass
